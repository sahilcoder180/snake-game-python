
import pygame
import random
import sys
from pygame.math import Vector2

pygame.init()

#Phone ki full screen
info = pygame.display.Info()
W = info.current_w
H = info.current_h
CELL_SIZE = 40
CELL_NUMBER_X = W // CELL_SIZE
CELL_NUMBER_Y = H // CELL_SIZE

screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
clock = pygame.time.Clock()

#Colors
GREEN = (175, 215, 70)
DARK_GREEN = (56, 142, 60)
RED = (255, 0, 0)
BLUE = (50, 100, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

font = pygame.font.Font(None, int(W / 15))

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self):
        for i, block in enumerate(self.body):
            x = int(block.x * CELL_SIZE)
            y = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if i == 0:
                pygame.draw.rect(screen, BLUE, block_rect)
                pygame.draw.rect(screen, WHITE, block_rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GREEN, block_rect)
                pygame.draw.rect(screen, GREEN, block_rect, 3)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw(self):
        x = int(self.pos.x * CELL_SIZE)
        y = int(self.pos.y * CELL_SIZE)
        fruit_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.ellipse(screen, RED, fruit_rect)
        pygame.draw.ellipse(screen, WHITE, fruit_rect, 3)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER_X - 1)
        self.y = random.randint(2, CELL_NUMBER_Y - 6)
        self.pos = Vector2(self.x, self.y)

class BUTTON:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 4)
        text_surf = font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.rect.centerx - text_surf.get_width() // 2,
                                self.rect.centery - text_surf.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0
        self.game_over = False

        # Button sab dikhenge - upar kar diye
        btn_size = W // 6
        margin = 50
        self.btn_up = BUTTON(W//2 - btn_size//2, H - btn_size*3 - margin, btn_size, btn_size, "▲")
        self.btn_down = BUTTON(W//2 - btn_size//2, H - btn_size*1.5 - margin, btn_size, btn_size, "▼")
        self.btn_left = BUTTON(W//2 - btn_size*1.8, H - btn_size*2.25 - margin, btn_size, btn_size, "◀")
        self.btn_right = BUTTON(W//2 + btn_size*0.8, H - btn_size*2.25 - margin, btn_size, btn_size, "▶")

    def update(self):
        if not self.game_over:
            self.snake.move()
            self.check_collision()
            self.check_fail()

    def draw(self):
        self.draw_grass()
        self.fruit.draw()
        self.snake.draw()
        self.draw_score()
        self.draw_buttons()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER_X or not 0 <= self.snake.body[0].y < CELL_NUMBER_Y - 6:
            self.game_over = True
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over = True

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER_Y):
            for col in range(CELL_NUMBER_X):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        if self.game_over:
            over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Tap anywhere to Restart", True, BLACK)
            screen.blit(over_text, (W//2 - over_text.get_width()//2, H//2 - 100))
            screen.blit(restart_text, (W//2 - restart_text.get_width()//2, H//2 - 40))

    def draw_buttons(self):
        if not self.game_over:
            self.btn_up.draw()
            self.btn_down.draw()
            self.btn_left.draw()
            self.btn_right.draw()

touch_start = None
game = GAME()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.game_over:
                game = GAME()
            else:
                touch_start = event.pos
                if game.btn_up.is_clicked(event.pos) and game.snake.direction.y!= 1:
                    game.snake.direction = Vector2(0, -1)
                elif game.btn_down.is_clicked(event.pos) and game.snake.direction.y!= -1:
                    game.snake.direction = Vector2(0, 1)
                elif game.btn_left.is_clicked(event.pos) and game.snake.direction.x!= 1:
                    game.snake.direction = Vector2(-1, 0)
                elif game.btn_right.is_clicked(event.pos) and game.snake.direction.x!= -1:
                    game.snake.direction = Vector2(1, 0)

        if event.type == pygame.MOUSEBUTTONUP and touch_start:
            if not game.game_over:
                dx = event.pos[0] - touch_start[0]
                dy = event.pos[1] - touch_start[1]
                if abs(dx) > abs(dy) and abs(dx) > 50:
                    if dx > 0 and game.snake.direction.x!= -1:
                        game.snake.direction = Vector2(1, 0)
                    elif dx < 0 and game.snake.direction.x!= 1:
                        game.snake.direction = Vector2(-1, 0)
                elif abs(dy) > abs(dx) and abs(dy) > 50:
                    if dy > 0 and game.snake.direction.y!= -1:
                        game.snake.direction = Vector2(0, 1)
                    elif dy < 0 and game.snake.direction.y!= 1:
                        game.snake.direction = Vector2(0, -1)
            touch_start = None

    screen.fill(GREEN)
    game.draw()
    pygame.display.update()
    clock.tick(60)

import pygame
import sys
from pygame.locals import *
from random import randrange as rand


pygame.init()

WIDTH_OF_MAIN_SCREEN, HEIGHT_OF_MAIN_SCREEN = 1200, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORE = 0

screen = pygame.display.set_mode((WIDTH_OF_MAIN_SCREEN, HEIGHT_OF_MAIN_SCREEN))
pygame.display.set_caption("Arkanoid")

font = pygame.font.Font(None, 36)

paddle_weight = 330
paddle_height = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH_OF_MAIN_SCREEN // 2 - paddle_weight // 2, HEIGHT_OF_MAIN_SCREEN - paddle_height - 10,
                     paddle_weight, paddle_height)

ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rand(ball_rect, WIDTH_OF_MAIN_SCREEN - ball_rect), HEIGHT_OF_MAIN_SCREEN // 2, ball_rect, ball_rect)
dx, dy = 1, -1

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rand(30, 256), rand(30, 256), rand(30, 256))
              for i in range(10) for j in range(4)]

clock = pygame.time.Clock()

background_image = pygame.image.load('1.jpeg').convert()


def print_the_text(text, x, y):
    surface = font.render(text, True, WHITE)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        self.image = pygame.Surface((200, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.text = text

    def update(self):
        print_the_text(self.text, self.rect.centerx, self.rect.centery)


def starting_the_game():
    global clock
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            the_game_cycle()

        screen.fill(BLACK)

        start_button.update()
        exit_button.update()

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def ball_collisions(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def the_game_cycle():
    global FPS, dx, dy, SCORE, font
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.blit(background_image, (0, 0))

        [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(screen, pygame.Color('darkorange'), paddle)

        pygame.draw.circle(screen, pygame.Color('white'), ball.center, ball_radius)

        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

        if ball.centerx < ball_radius or ball.centerx > WIDTH_OF_MAIN_SCREEN - ball_radius:
            dx = -dx

        if ball.centery < ball_radius:
            dy = -dy

        if ball.colliderect(paddle) and dy > 0:
            dx, dy = ball_collisions(dx, dy, ball, paddle)

        hit_index = ball.collidelist(block_list)

        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = ball_collisions(dx, dy, ball, hit_rect)

            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(screen, hit_color, hit_rect)
            FPS += 2
            SCORE += 1

        if ball.bottom > HEIGHT_OF_MAIN_SCREEN:
            game_over()
            exit()
        elif not len(block_list):
            you_win()
            print('WIN!!!')
            exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < WIDTH_OF_MAIN_SCREEN:
            paddle.right += paddle_speed

        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(SCORE), True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    global clock
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(BLACK)

        print_the_text("Game Over", WIDTH_OF_MAIN_SCREEN // 2, HEIGHT_OF_MAIN_SCREEN // 2)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def you_win():
    global clock
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(BLACK)

        print_the_text("You Win!", WIDTH_OF_MAIN_SCREEN // 2, HEIGHT_OF_MAIN_SCREEN // 2)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


start_button = Button("Start (PRESS SPACE)", WIDTH_OF_MAIN_SCREEN // 2, HEIGHT_OF_MAIN_SCREEN // 2 - 50)
exit_button = Button("Exit", WIDTH_OF_MAIN_SCREEN // 2, HEIGHT_OF_MAIN_SCREEN // 2 + 50)

start_game = True
while start_game:
    for event in pygame.event.get():
        if event.type == QUIT:
            start_game = False

    keys = pygame.key.get_pressed()
    if keys[K_SPACE]:
        the_game_cycle()

    screen.fill(BLACK)

    start_button.update()
    exit_button.update()

    pygame.display.flip()

pygame.quit()
sys.exit()

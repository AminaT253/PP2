import pygame
import random
import sys

pygame.init()

Screen_w, Screen_h = 600, 400
Cell_size = 20
screen = pygame.display.set_mode((Screen_w, Screen_h))
pygame.display.set_caption("Snake Game")
Clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 19)

Blue  = (0, 0, 255)
Red   = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)
White = (255, 255, 255)

def draw_walls():
    pygame.draw.rect(screen, Blue, (0, 0, Screen_w, Cell_size))
    pygame.draw.rect(screen, Blue, (0, Screen_h - Cell_size, Screen_w, Cell_size))
    pygame.draw.rect(screen, Blue, (0, 0, Cell_size, Screen_h))
    pygame.draw.rect(screen, Blue, (Screen_w - Cell_size, 0, Cell_size, Screen_h))

def food_generator(snake):
    while True:
        x = random.randint(1, (Screen_w - Cell_size * 2) // Cell_size) * Cell_size
        y = random.randint(1, (Screen_h - Cell_size * 2) // Cell_size) * Cell_size
        food = (x, y) 
        if food not in snake:
            return food

def game():
    snake = [(Cell_size * 10, Cell_size * 10)]
    direction = (Cell_size, 0)
    food = food_generator(snake)
    score = 0
    level = 1
    speed = 3

    while True:
        screen.fill(White)
        draw_walls()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, Cell_size):
                    direction = (0, -Cell_size)
                elif event.key == pygame.K_DOWN and direction != (0, -Cell_size):
                    direction = (0, Cell_size)
                elif event.key == pygame.K_LEFT and direction != (Cell_size, 0):
                    direction = (-Cell_size, 0)
                elif event.key == pygame.K_RIGHT and direction != (-Cell_size, 0):
                    direction = (Cell_size, 0)

        new_pos = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (new_pos in snake or 
            new_pos[0] < Cell_size or new_pos[0] >= Screen_w - Cell_size or 
            new_pos[1] < Cell_size or new_pos[1] >= Screen_h - Cell_size):
            break

        snake.insert(0, new_pos)

        if new_pos == food:
            score += 1
            food = food_generator(snake)

            if score % 3 == 0:
                level += 1
                speed += 2

        else:
            snake.pop()

        for part in snake:
            pygame.draw.rect(screen, Green, (*part, Cell_size, Cell_size))

        pygame.draw.rect(screen, Red, (*food, Cell_size, Cell_size))

        score_text = font.render(f"Score: {score}", True, Black)
        level_text = font.render(f"Level: {level}", True, Black)

        screen.blit(score_text, (0, 0))
        screen.blit(level_text, (Screen_w - 100, 0))

        pygame.display.flip()
        Clock.tick(speed)

game()
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
Yellow = (255, 255, 0)
Orange = (255, 100, 10)
Green = (0, 255, 0)
Black = (0, 0, 0)
White = (255, 255, 255)

def draw_walls():
    pygame.draw.rect(screen, Blue, (0, 0, Screen_w, Cell_size))
    pygame.draw.rect(screen, Blue, (0, Screen_h - Cell_size, Screen_w, Cell_size))
    pygame.draw.rect(screen, Blue, (0, 0, Cell_size, Screen_h))
    pygame.draw.rect(screen, Blue, (Screen_w - Cell_size, 0, Cell_size, Screen_h))

class Food():

    def __init__(self, snake, speed):
        self.value = random.choice([1, 2, 3])
        self.color = {1: Yellow, 2: Orange, 3: Red}[self.value]
        self.position = self.generate_position(snake)
        self.timer = 5 * speed 

    def generate_position(self, snake):
        while True:
            x = random.randint(1, (Screen_w - Cell_size * 2) // Cell_size) * Cell_size
            y = random.randint(1, (Screen_h - Cell_size * 2) // Cell_size) * Cell_size
            if (x, y) not in snake:
                return (x, y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (*self.position, Cell_size, Cell_size))

    def update_timer(self):
        self.timer -= 1
        return self.timer <= 0

def game():
    snake = [(Cell_size * 10, Cell_size * 10)]
    direction = (Cell_size, 0)
    score = 0
    level = 1
    speed = 3
    food = Food(snake, speed)

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

        if new_pos == food.position:
            score += food.value
            food = Food(snake, speed)

            if score % 5 == 0:
                level += 1
                speed += 2

        else:
            snake.pop()
        
        if food.update_timer():
            food = None

        if food is None:
            food = Food(snake, speed)
        else:
            food.draw()

        for part in snake:
            pygame.draw.rect(screen, Green, (*part, Cell_size, Cell_size))

        
        score_text = font.render(f"Score: {score}", True, Black)
        level_text = font.render(f"Level: {level}", True, Black)

        screen.blit(score_text, (0, 0))
        screen.blit(level_text, (Screen_w - 100, 0))

        pygame.display.flip()
        Clock.tick(speed)

game()
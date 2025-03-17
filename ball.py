import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("The Ball")

radius = 25
x, y = 400, 300
move = 20

red = (255, 0, 0)
white = (255, 255, 255)

running = True
while running:
    
    screen.fill(white)

    current_pos = (400, 300)
    pygame.draw.circle(screen, red, (x, y), radius)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and y - radius - move >= 0:
                y -= move

            elif event.key == pygame.K_DOWN and y + radius + move <= 600:
                y += move

            elif event.key == pygame.K_LEFT and x - radius - move >= 0:
                x -= move

            elif event.key == pygame.K_RIGHT and x + radius + move <= 800:
                x += move


    

    pygame.display.flip()

pygame.quit()
sys.exit()
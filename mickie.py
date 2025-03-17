import pygame
import datetime
import sys

pygame.init()

size = width, height = 600, 600
center = (300, 300)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mickey Clock")

white = (255, 255, 255)
black = (0, 0, 0)

Clock = pygame.time.Clock()

the_clock = pygame.image.load('images/mickeyclock.jpg')
clock_w = 500
clock_h = 500
clock_x = (300 - clock_w/2)
clock_y = (300 - clock_h/2)


big_arrow = pygame.image.load('images/bigarrow.png')
big_arrow_w = 60
big_arrow_h = 250
big_arrow = pygame.transform.scale(big_arrow, (big_arrow_w, big_arrow_h))

big_arrow_rect = big_arrow.get_rect()
big_arrow_rect.center = center


small_arrow = pygame.image.load('images/smallarrow.png')
small_arrow_w = 30
small_arrow_h = 300
small_arrow = pygame.transform.scale(small_arrow, (small_arrow_w, small_arrow_h))

small_arrow_rect = small_arrow.get_rect()
small_arrow_rect.center = center

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False

    
    screen.fill(white)
    screen.blit(the_clock, (clock_x, clock_y))

    angle_second = datetime.datetime.now().second * -6
    rotated_big_arrow = pygame.transform.rotate(big_arrow, angle_second)
    rotated_big_arrow_rect = rotated_big_arrow.get_rect()
    rotated_big_arrow_rect.center = big_arrow_rect.center
    screen.blit(rotated_big_arrow, rotated_big_arrow_rect)

    angle_minute = datetime.datetime.now().minute * -6
    rotated_small_arrow = pygame.transform.rotate(small_arrow, angle_minute)
    rotated_small_arrow_rect = rotated_small_arrow.get_rect()
    rotated_small_arrow_rect.center = small_arrow_rect.center
    screen.blit(rotated_small_arrow, rotated_small_arrow_rect)


    pygame.display.flip()
    Clock.tick(60)

pygame.quit()
sys.exit()

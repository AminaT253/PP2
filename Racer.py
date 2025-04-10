import pygame
import sys
import random

pygame.init()

FPS = 60
Clock = pygame.time.Clock()

Blue  = (0, 0, 255)
Red   = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)
White = (255, 255, 255)

Screen_w = 500
Screen_h = 700

Display_surface = pygame.display.set_mode((Screen_w, Screen_h))
Display_surface.fill(White)
pygame.display.set_caption("Racer game")

back_stage = pygame.image.load("images/race.png")
back_stage = pygame.transform.scale(back_stage, (500, 700))

Font = pygame.font.SysFont("Verdana", 25)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (70, 130))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, Screen_w - 40), 0)
        self.speed = 5

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > Screen_h:
            self.rect.top = 0
            self.rect.center = (random.randint(40, Screen_w - 40), 0)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Player.png")
        self.image = pygame.transform.scale(self.image, (70, 130))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 450)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < 500:
            self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

coin_images = {
    1: pygame.transform.scale(pygame.image.load("images/Yuan.png"), (40, 40)),
    2: pygame.transform.scale(pygame.image.load("images/Dollar.png"), (50, 50)),
    3: pygame.transform.scale(pygame.image.load("images/Euro.png"), (60, 60))
}
coin_values = [1, 2, 3]

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice(coin_values)
        self.image = coin_images[self.value]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, Screen_w - 40), random.randint(-100, -40))

    def move(self):
        self.rect.move_ip(0, 3)
        if self.rect.top > Screen_h:
            self.reset_position()

    def reset_position(self):
        self.value = random.choice(coin_values)
        self.image = coin_images[self.value]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, Screen_w - 40), random.randint(-100, -40))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()

for _ in range(1):
    coins.add(Coin())

coin_score = 0
new_speed_coin = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    Display_surface.blit(back_stage, (0, 0))

    P1.update()
    E1.move()
    for coin in coins:
        coin.move()

    for coin in coins:
        if P1.rect.colliderect(coin.rect):
            coin_score += coin.value
            coin.reset_position()

            if coin_score % new_speed_coin == 0:
                E1.speed += 1

    if P1.rect.colliderect(E1.rect):
        game_over_text = Font.render("GAME OVER", True, Red)
        Display_surface.blit(game_over_text, (180, 350))
        pygame.display.update()
        pygame.time.delay(1000)  
        pygame.quit()
        sys.exit()

    P1.draw(Display_surface)
    E1.draw(Display_surface)
    for coin in coins:
        coin.draw(Display_surface)

    score_text = Font.render(f"Coins : {coin_score}", True, Black)
    Display_surface.blit(score_text, (250, 10))

    pygame.display.update()
    Clock.tick(FPS)


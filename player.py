import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music Player")

Music_list = [
    'music_set/Dance_monkey.mp3',
    'music_set/Kukla_kolduna.mp3',
    'music_set/Po_baram.mp3'
]

current_track = 0
pygame.mixer.music.load(Music_list[0])
pygame.mixer.music.play()

the_player = pygame.image.load('player.png')
the_player = pygame.transform.scale(the_player, (800, 600))

black = (0, 0, 0)
is_playing = True

running = True
while running:

    screen.fill(black)
    screen.blit(the_player, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_playing:
                    pygame.mixer.music.pause()  
                    is_playing = False     
                else:
                    pygame.mixer.music.unpause() 
                    is_playing = True

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                is_playing = False

            elif event.key == pygame.K_n:
                current_track = (current_track + 1) % len(Music_list)
                pygame.mixer.music.load(Music_list[current_track])
                pygame.mixer.music.play()
                is_playing = True

            elif event.key == pygame.K_p:
                current_track = (current_track - 1) % len(Music_list)
                pygame.mixer.music.load(Music_list[current_track])
                pygame.mixer.music.play()
                is_playing = True




    pygame.display.flip()

pygame.quit()
sys.exit()
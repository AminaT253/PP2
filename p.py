import pygame
import sys

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music Player")

# Load music list
music_list = [
    'music/Po_baram.mp3',
    'music/Kukla_kolduna.mp3',
    'music/Dance_monkey.mp3'
]
current_track = 0  # Start with the first track

# Load and start playing the first song
pygame.mixer.music.load(music_list[current_track])
pygame.mixer.music.play()

# Load player image
the_player = pygame.image.load('player.png')
the_player_scaled = pygame.transform.scale(the_player, (700, 500))

# Flags
is_playing = True

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))  # Background color
    screen.blit(the_player_scaled, (50, 50))  # Draw the player image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Play / Pause (SPACE)
            if event.key == pygame.K_SPACE:
                if is_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                is_playing = not is_playing  # Toggle flag

            # Stop Music (S)
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                is_playing = False

            # Next Track (N)
            elif event.key == pygame.K_n:
                current_track = (current_track + 1) % len(music_list)
                pygame.mixer.music.load(music_list[current_track])
                pygame.mixer.music.play()
                is_playing = True  # Ensure playing state is updated

            # Previous Track (P)
            elif event.key == pygame.K_p:
                current_track = (current_track - 1) % len(music_list)
                pygame.mixer.music.load(music_list[current_track])
                pygame.mixer.music.play()
                is_playing = True  # Ensure playing state is updated

    pygame.display.flip()

pygame.quit()
sys.exit()

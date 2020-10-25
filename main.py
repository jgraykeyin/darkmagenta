import pygame
import os
import random

pygame.init()

# Color palette
light_cyan = (85,255,255)
dark_cyan = (0,170,170)
dark_green = (0,170,0)
light_green = (85,255,85)

# Set file location to current directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Tile and display sizes
tile_size = 96
display_width = 9
display_height = 7
step=24

# Setup the main game display
game_display = pygame.display.set_mode((display_width*tile_size,display_height*tile_size))
pygame.display.set_caption('Dark Magenta')

# Initialize the game clock
clock = pygame.time.Clock()

# Load character sprite
player = pygame.image.load(os.path.join(__location__,'magenta_start.png'))

# Setup the main game loop
def game_loop():
    player_pos = [0,1]

    game_exit = False

    while not game_exit:
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_pos[0] += step
                elif event.key == pygame.K_LEFT:
                    player_pos[0] -= step

        # Paint the screen with background color
        game_display.fill(dark_cyan)

        # Draw the player character
        game_display.blit(player,(player_pos[0],player_pos[1]))

        # Update the screen
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()

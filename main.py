import pygame
import os
import random
import math

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
game_display = pygame.display.set_mode((display_width*tile_size,display_height*tile_size+50))
pygame.display.set_caption('Dark Magenta')

# Initialize the game clock
clock = pygame.time.Clock()

# Load character sprite
player = pygame.image.load(os.path.join(__location__,'magenta_start.png'))
player_walk = pygame.image.load(os.path.join(__location__,'magenta_walk.png'))

# Load in sound effects
walk_sound = pygame.mixer.Sound(os.path.join(__location__,'sound_walk.wav'))
walk_sound.set_volume(0.5)

# Setup tile types
blank_tile = 0
grass1_tile = 1
grass2_tile = 2
mush1_tile = 3
mush2_tile = 4

tile_textures = {
    blank_tile: pygame.image.load(os.path.join(__location__,'blank_tile.png')),
    grass1_tile: pygame.image.load(os.path.join(__location__,'grass1.png')),
    grass2_tile: pygame.image.load(os.path.join(__location__,'grass2.png')),
    mush1_tile: pygame.image.load(os.path.join(__location__,'mush1.png')),
    mush2_tile: pygame.image.load(os.path.join(__location__,'mush2.png')),
}

# Setup collectable resources
resources = [mush1_tile,mush2_tile]

# Initialize inventory
inventory_font = pygame.font.Font(os.path.join(__location__,'PressStart2P-Regular.ttf'),18)
inventory = {
    mush1_tile:0,
    mush2_tile:0
}

# Create a full map of blank tiles
tile_map = [[blank_tile for w in range(display_width)] for h in range(display_height)]

# Generate the map
for row in range(display_height):
    for col in range(display_width):
        num = random.randint(0,15)
        if num == 0:
            tile = blank_tile
        elif num in [1,2,3,4,5,6,7,8,9]:
            tile = grass1_tile
        elif num in [10,11,12]:
            tile = mush1_tile
        elif num in [13,14,15]:
            tile = mush2_tile
        tile_map[row][col] = tile


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
                if event.key == pygame.K_RIGHT and player_pos[0] < ((display_width * tile_size) - tile_size):
                    player_pos[0] += step
                    walk_sound.play()
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= step
                    walk_sound.play()
                elif event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= step
                    walk_sound.play()
                elif event.key == pygame.K_DOWN and player_pos[1] < ((display_height * tile_size) - tile_size):
                    player_pos[1] += step
                    walk_sound.play()
                if event.key == pygame.K_SPACE:
                    # Pick-up mushroom if it's available on current tile
                    py = math.floor(player_pos[1]/tile_size)
                    px = math.floor(player_pos[0]/tile_size)
                    current_tile = tile_map[py][px]
                    if current_tile == 3 or current_tile == 4:
                        # Add mushroom to inventory
                        inventory[current_tile] += 1
                        # Replace with blank tile
                        tile_map[py][px] = blank_tile
                    else:
                        pass
                    
        # Paint the screen with background color
        game_display.fill(dark_cyan)

        # Draw the map
        for row in range(display_height):
            for column in range(display_width):
                game_display.blit(tile_textures[tile_map[row][column]],(column*tile_size,row*tile_size))

        # Draw the player character
        game_display.blit(player,(player_pos[0],player_pos[1]))

        # Update the screen
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()

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
player_flip = pygame.transform.flip(player,1,0)
player_walk = pygame.image.load(os.path.join(__location__,'magenta_walk.png'))
player_walk_flip = pygame.transform.flip(player_walk,1,0)
# Load the cat sprite
cat1 = pygame.image.load(os.path.join(__location__,'cat1.png'))
cat2 = pygame.image.load(os.path.join(__location__,'cat2.png'))

# Load in sound effects
walk_sound = pygame.mixer.Sound(os.path.join(__location__,'sound_walk.wav'))
walk_sound.set_volume(0.5)
get_item_sound = pygame.mixer.Sound(os.path.join(__location__,'get_item.wav'))
get_item_sound.set_volume(0.4)

# Repeat ambient background sounds
pygame.mixer.music.load(os.path.join(__location__, "forestsounds.mp3"))
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1,8000)

# Setup tile types
blank_tile = 0
grass1_tile = 1
water_tile = 2
mush1_tile = 3
mush2_tile = 4
spore_tile = 5

tile_textures = {
    blank_tile: pygame.image.load(os.path.join(__location__,'blank_tile.png')),
    grass1_tile: pygame.image.load(os.path.join(__location__,'grass1.png')),
    water_tile: pygame.image.load(os.path.join(__location__,'pond1.png')),
    mush1_tile: pygame.image.load(os.path.join(__location__,'mush1.png')),
    mush2_tile: pygame.image.load(os.path.join(__location__,'mush2.png')),
    spore_tile: pygame.image.load(os.path.join(__location__,'spores.png')),
}

# Frames for animation
water2_tile =  pygame.image.load(os.path.join(__location__,'pond2.png'))
grass2_tile = pygame.image.load(os.path.join(__location__,'grass2.png'))

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
        elif num in [1,2,3,4,5,6,7,8]:
            tile = grass1_tile
        elif num == 9:
            tile = water_tile
        elif num in [10,11,12]:
            tile = mush1_tile
        elif num in [13,14,15]:
            tile = mush2_tile
        tile_map[row][col] = tile


# Setup the main game loop
def game_loop():
    player_pos = [0,0]
    cat_pos = [(display_width*tile_size)-tile_size,(display_height*tile_size)-tile_size]
    frame_count = 0
    wind=0
    walk=0
    direction=0
    game_exit = False

    while not game_exit:
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                # Trying to use this to stop player from walking into water
                current_tile = tile_map[math.floor(player_pos[1]/tile_size)][math.floor(player_pos[0]/tile_size)]

                if event.key == pygame.K_RIGHT and player_pos[0] < ((display_width * tile_size) - tile_size):
                    player_pos[0] += step
                    walk_sound.play()
                    walk=1
                    direction=0
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= step
                    walk_sound.play()
                    walk=1
                    direction=1
                elif event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= step
                    walk_sound.play()
                    walk=1
                elif event.key == pygame.K_DOWN and player_pos[1] < ((display_height * tile_size) - tile_size):
                    player_pos[1] += step
                    walk_sound.play()
                    walk=1
                if event.key == pygame.K_SPACE:
                    # Pick-up mushroom if it's available on current tile
                    py = math.floor(player_pos[1]/tile_size)
                    px = math.floor(player_pos[0]/tile_size)
                    current_tile = tile_map[py][px]
                    if current_tile == 3 or current_tile == 4:
                        # Add mushroom to inventory
                        inventory[current_tile] += 1
                        # Replace with spore tile
                        tile_map[py][px] = spore_tile
                        get_item_sound.play()

            # Reset the walking flag for proper walk animation
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    walk=0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    walk=0
                    
        # Paint the screen with background color
        game_display.fill(dark_cyan)

        # Increment the frame counter used to animate water
        frame_count+=1
        # Generate wind-change for grass
        wind_roll = random.randint(0,40)
        if wind_roll > 39:
            wind = 1

        # Draw the map
        for row in range(display_height):
            for column in range(display_width):
                    # Check for ponds, they must be animated
                    if tile_map[row][column] == 2 and frame_count <= 50:
                        game_display.blit(tile_textures[tile_map[row][column]],(column*tile_size,row*tile_size))
                    elif tile_map[row][column] == 2 and frame_count > 50:
                        game_display.blit(water2_tile,(column*tile_size,row*tile_size))
                    # Check for wind to animate grass
                    elif tile_map[row][column] == 1 and wind == 1:
                        game_display.blit(grass2_tile,(column*tile_size,row*tile_size))
                    else:
                        game_display.blit(tile_textures[tile_map[row][column]],(column*tile_size,row*tile_size))

        # Draw the cat sprite, also clear corner tiles for player & cat
        tile_map[0][0] = 0
        tile_map[6][8] = 0
        if frame_count % 20 == 0:
            cat_direction = random.randint(0,20)
            # 0:LEFT  1:RIGHT  2:DOWN  3:UP
            # Move cat left
            if cat_direction in [0,1,2,3,4,5,6,7] and cat_pos[0] > 0: 
                cat_pos[0] -= step
            # Move cat right
            elif cat_direction in [8,9,10,11,12,13] and cat_pos[0] < ((display_width * tile_size) - tile_size):
                cat_pos[0] += step
            # Move cat down
            elif cat_direction in [14,15,16] and cat_pos[1] < ((display_height * tile_size) - tile_size):
                cat_pos[1] += step
            # Move cat up
            elif cat_direction in [17,18,19,20] and cat_pos[1] > 0:
                cat_pos[1] -= step
            # Cat tries to eat mushroom if it's on a mushroom tile
            py = math.floor(cat_pos[1]/tile_size)
            px = math.floor(cat_pos[0]/tile_size)
            current_tile = tile_map[py][px]
            if current_tile == 3 or current_tile == 4:
                # Replace with spore tile
                tile_map[py][px] = spore_tile
                get_item_sound.play()
        if frame_count <= 50:
            game_display.blit(cat1,(cat_pos[0],cat_pos[1]))
        elif frame_count > 50:
            game_display.blit(cat2,(cat_pos[0],cat_pos[1]))

        # Draw the player character
        if walk == 0 and direction == 0:
            game_display.blit(player,(player_pos[0],player_pos[1]))
        elif walk == 0 and direction == 1:
            game_display.blit(player_flip,(player_pos[0],player_pos[1]))
        elif walk == 1 and direction == 0:
            game_display.blit(player_walk,(player_pos[0],player_pos[1]))
        elif walk == 1 and direction == 1:
            game_display.blit(player_walk_flip,(player_pos[0],player_pos[1]))

        # Update the screen
        pygame.display.update()
        clock.tick(60)
        if frame_count > 100:
            frame_count = 0
        wind_roll = random.randint(0,40)
        if wind_roll > 39:
            wind = 0

game_loop()
pygame.quit()
quit()

# Project Dark Magenta by Justin Gray.
# Pygame development project for a two player sprite-based collect & craft game.
# Players are controlled using A,W,S,D (player 1) and Left,Right,Up,Down (player 2).
# Each collectable mushroom has 2 levels of crafting, poison mushrooms reduce HP by 1.
#
# Music by 'sawsquarenoise` (CC BY 4.0 license)
# https://freemusicarchive.org/music/sawsquarenoise/
# 
# Sound effects from freesound.org
# Graphics drawn using piskelapp.com

import pygame
import os
import random
import math
import time

pygame.init()

# Color palette
light_cyan = (85,255,255)
dark_cyan = (0,170,170)
dark_green = (0,170,0)
light_green = (85,255,85)
magenta = (255,85,255)
dark_magenta = (170,0,170)
black = (0,0,0)

# Set file location to current directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Tile and display sizes
tile_size = 96
display_width = 9
display_height = 7
step=24

# Player Scores
score_p1 = 0
score_p2 = 0

# Setup the main game display
game_display = pygame.display.set_mode((display_width*tile_size,display_height*tile_size+50))
pygame.display.set_caption('Dark Magenta')

# Initialize the game clock
clock = pygame.time.Clock()

# Load P1 sprites
player = pygame.image.load(os.path.join(__location__,'images/magenta_start.png'))
player_flip = pygame.transform.flip(player,1,0)
player_walk = pygame.image.load(os.path.join(__location__,'images/magenta_walk.png'))
player_walk_flip = pygame.transform.flip(player_walk,1,0)
player_dmg = pygame.image.load(os.path.join(__location__,'images/p1_hit.png'))
player_dmg_flip = pygame.transform.flip(player_dmg,1,0)

# Load P2 sprites
cat_main = pygame.image.load(os.path.join(__location__,'images/cat_main.png'))
cat_main_flip = pygame.transform.flip(cat_main,1,0)
cat_eat = pygame.image.load(os.path.join(__location__,'images/cat_eat.png'))
cat_eat_flip = pygame.transform.flip(cat_eat,1,0)
cat_walk = pygame.image.load(os.path.join(__location__,'images/cat_walk.png'))
cat_walk_flip = pygame.transform.flip(cat_walk,1,0)
cat_dmg = pygame.image.load(os.path.join(__location__,'images/p2_hit.png'))
cat_dmg_flip = pygame.transform.flip(cat_dmg,1,0)

# Load in sound effects
walk_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/sound_walk.wav'))
walk_sound.set_volume(0.5)
get_item_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/get_item.wav'))
get_item_sound.set_volume(0.4)
cat_pickup_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/cat_pickup.mp3'))
cat_pickup_sound.set_volume(0.4)
poison_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/poison.mp3'))
poison_sound.set_volume(0.2)
craft_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/craftsound.mp3'))
craft_sound.set_volume(0.4)
water_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/water_dmg2.wav'))
water_sound.set_volume(0.1)
hit_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/hit.wav'))
hit_sound.set_volume(0.4)
shing_menu_sound = pygame.mixer.Sound(os.path.join(__location__,'audio/shining.wav'))
shing_menu_sound.set_volume(0.3)

# Setup tile types
blank_tile = 0
grass1_tile = 1
water_tile = 2
mush1_tile = 3
mush2_tile = 4
spore_tile = 5
mush3_tile = 6
camp_tile = 7
heart_tile = 8
mush4_tile = 9
speed_tile = 10
exitfire_tile = 11
exitdoor_tile = 12

tile_textures = {
    blank_tile: pygame.image.load(os.path.join(__location__,'images/blank_tile.png')),
    grass1_tile: pygame.image.load(os.path.join(__location__,'images/grass1.png')),
    water_tile: pygame.image.load(os.path.join(__location__,'images/pond1.png')),
    mush1_tile: pygame.image.load(os.path.join(__location__,'images/mush1.png')),
    mush2_tile: pygame.image.load(os.path.join(__location__,'images/mush4.png')),
    spore_tile: pygame.image.load(os.path.join(__location__,'images/spores.png')),
    mush3_tile: pygame.image.load(os.path.join(__location__,'images/mush3.png')),
    camp_tile: pygame.image.load(os.path.join(__location__,'images/campfire1.png')),
    heart_tile: pygame.image.load(os.path.join(__location__,'images/heart_icon.png')),
    mush4_tile: pygame.image.load(os.path.join(__location__,'images/mush5.png')),
    speed_tile: pygame.image.load(os.path.join(__location__,'images/speed_icon.png')),
    exitfire_tile: pygame.image.load(os.path.join(__location__,'images/exit_fire1.png')),
    exitdoor_tile: pygame.image.load(os.path.join(__location__,'images/door_exit.png'))
}

# Frames for animation
water2_tile =  pygame.image.load(os.path.join(__location__,'images/pond2.png'))
grass2_tile = pygame.image.load(os.path.join(__location__,'images/grass2.png'))
camp2_tile = pygame.image.load(os.path.join(__location__,'images/campfire2.png'))
exitfire2_tile = pygame.image.load(os.path.join(__location__,'images/exit_fire2.png'))

# Main Menu Graphic
main_menu_image = pygame.image.load(os.path.join(__location__,'images/startup_screen.png'))
magenta_fly = pygame.image.load(os.path.join(__location__,'images/magenta_fly.png'))

# Setup collectable resources
resources = [mush1_tile,mush2_tile,mush3_tile,heart_tile]

# Initialize P1 inventory
inventory_font = pygame.font.Font(os.path.join(__location__,'PressStart2P-Regular.ttf'),16)

def scorePoint(player,points):
    '''
    Description: Add points to P1 or P2
    Parameters:
        player - "p1" or "p2"
        points - amount of points to add
    Returns: Nothing
    '''
    global score_p1
    global score_p2

    if player == "p1":
        score_p1 += points
    elif player == "p2":
        score_p2 += points

def generateMap():
    '''
    Descriptions: Generates a tiled map at the start of a round
    Parameters: None
    Returns:
        List of tile numbers
    '''

    # Create a full map of blank tiles
    tile_map = [[blank_tile for w in range(display_width)] for h in range(display_height)]

    # Generate the map
    for row in range(display_height):
        for col in range(display_width):
            num = random.randint(0,20)
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
            elif num in [16,17,18]:
                tile = mush3_tile
            elif num in [19,20]:
                tile = mush4_tile
            tile_map[row][col] = tile
    # Clear corner tiles for player & cat
    tile_map[0][0] = 0
    tile_map[6][8] = 0

    # Select a random tile and place the campfire
    r_row = random.randint(1,display_height-1)
    r_col = random.randint(1,display_width-1)
    tile_map[r_row][r_col] = camp_tile

    return tile_map

def resetInventory():
    '''
    Description: Initializes the inventory for the beginning of a match
    Parameters: None
    Returns:
        List of inventory items
    '''
    inventory = {
        mush1_tile:0,
        mush2_tile:0,
        mush3_tile:0,
        heart_tile:3
    }
    return inventory

# Draw a crafting message onto the screen for a moment when players craft
def craft_message(msg):
    '''
    Descriptions: Displays a message on the screen during gameplay
    Parameters:
        msg - Message that will be displayed as a string
    Returns: Nothing
    '''
    font = pygame.font.Font(os.path.join(__location__,'PressStart2P-Regular.ttf'), 32)
    text = font.render(msg,True,magenta,light_cyan)
    textRect = text.get_rect()
    textRect.center = ((display_width*tile_size) / 2, (display_height*tile_size) / 2)
    game_display.blit(text,textRect)
    pygame.display.update()
    time.sleep(1)


# Spore magic is a craftable spell that turns most mushrooms into poison
def spore_magic(tile_map):
    '''
    Description: Checks every mushroom on the board with a chance of changing it to a poison mushroom
    Parameters:
        tile_map - Tilemap to check, should be the game's current map
    Returns: Nothing
    '''
    for row in range(display_height):
        for col in range(display_width):
            # Chance of turning every mushroom into a poison mushroom
            roll = random.randint(0,20)
            if tile_map[row][col] in [3,4,6] and roll < 15:
                tile_map[row][col] = 9
                    

# Function to display the logo and prompt user to press enter to play
def main_menu():
    '''
    Description: Main menu that will display a graphic and wait for the user to start the game
    Parameters: None
    Returns: Nothing
    '''
    # Start the menu graphic at the bottom of the screen so we can scroll it upwards
    menu_height = 700
    menu_move = 0
    shing = 0
    shing_position = -900
    game_begin = False

    # Start playing main menu music
    pygame.mixer.music.load(os.path.join(__location__, "audio/menu_music.mp3"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    while not game_begin:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_begin = True

        game_display.fill(black)
        if menu_move % 20 == 0 and menu_height > 50:
            menu_height -= 2
        elif menu_height <= 50 and shing == 0:
            # Make that shiiiing sound that NES games would do on the title screens
            shing_menu_sound.play()
            game_display.fill(light_cyan)
            shing=1
        
        game_display.blit(main_menu_image,(20,menu_height))

        if shing == 1:
            shing_position += 40
            game_display.blit(magenta_fly,(shing_position,360))

        pygame.display.update()
        clock.tick(60)

def game_over():
    '''
    Description: End-game screen that displays the score and waits for the user to play again or quit the program
    Parameters: None
    Returns: Nothing
    '''
    game_end_state = True
    
    # Start playing game-over music
    pygame.mixer.music.load(os.path.join(__location__, "audio/game_end.mp3"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(1)

    while game_end_state:

        game_display.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_end_state = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gfont = pygame.font.Font(os.path.join(__location__,'PressStart2P-Regular.ttf'),24)

        game_over_title = gfont.render("Match Over!", True, dark_magenta, light_cyan)
        p1_score = gfont.render("P1 Score: {}".format(score_p1),True, dark_magenta, light_cyan)
        p2_score = gfont.render("P2 Score: {}".format(score_p2),True, dark_magenta, light_cyan)
        play_again = gfont.render("Press [ENTER] to play again",True, dark_magenta, light_cyan)

        w_center = 300
        game_display.blit(game_over_title, (w_center,260))
        game_display.blit(p1_score, (w_center,340))
        game_display.blit(p2_score, (w_center,380))
        game_display.blit(play_again, (w_center-180,440))

        pygame.display.update()


# Setup the main game loop
def game_loop():
    '''
    Description: The main gameplay loop that initializes many of our settings and loads the generated tilemap. 
                 We then check for keyboard events to move the characters on the screen.
    Parameters: None
    Returns: Nothing
    '''
    player_pos = [0,0]
    cat_pos = [(display_width*tile_size)-tile_size,(display_height*tile_size)-tile_size]

    inventory = resetInventory()
    inventory_cat = resetInventory()
    tile_map = generateMap()

    cat_walk_dir = 0
    cat_walking = 0
    nom=0
    frame_count = 0
    wind=0
    walk=0
    direction=0
    speed_bonus_p1 = 0
    speed_count_p1 = 200
    speed_bonus_p2 = 0
    speed_count_p2 = 200
    orbs_p1=0
    orbs_p2=0
    p1_dmg = 0
    p2_dmg = 0
    game_exit = False
    player_collide = 0

    # Start playing game music
    pygame.mixer.music.load(os.path.join(__location__, "audio/bgmusic1.mp3"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


    while not game_exit:
        # Check for player vs player collisions here
        collide_x = abs(player_pos[0] - cat_pos[0])
        collide_y = abs(player_pos[1] - cat_pos[1])
        if collide_x <= tile_size/2+24:
            #print("X collide {},{}".format(player_pos[0],cat_pos[0]))
            if collide_y <= tile_size/2+24:
                #print("Y collide {},{}".format(player_pos[1],cat_pos[1]))
                player_collide = 1
            else:
                player_collide = 0
        else:
            player_collide = 0


        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                current_tile = tile_map[math.floor(player_pos[1]/tile_size)][math.floor(player_pos[0]/tile_size)]
                current_cat_tile = tile_map[math.floor(cat_pos[1]/tile_size)][math.floor(cat_pos[0]/tile_size)]

                # Keep the corner tiles clear unless a crafted item is there
                if tile_map[0][0] != 8 and tile_map[0][0] != 10:
                    tile_map[0][0] = 0
                
                if tile_map[6][8] != 8 and tile_map[6][8] != 10:
                    tile_map[6][8] = 0

                if event.key == pygame.K_d and player_pos[0] < ((display_width * tile_size) - tile_size) and player_collide == 0:
                    player_pos[0] += step + speed_bonus_p1
                    walk_sound.play()
                    walk=1
                    direction=0
                # Check for a player collision and knock the character back
                if event.key == pygame.K_d and player_pos[0] < ((display_width * tile_size) - tile_size) and player_collide == 1:
                    player_pos[0] -= step*2
                    cat_pos[0] += step
                    hit_sound.play()
                    walk=1
                    direction=0
                elif event.key == pygame.K_a and player_pos[0] > 0 and player_collide == 0:
                    player_pos[0] -= step + speed_bonus_p1
                    walk_sound.play()
                    walk=1
                    direction=1
                elif event.key == pygame.K_a and player_pos[0] > 0 and player_collide == 1:
                    player_pos[0] += step*2
                    cat_pos[0] -= step
                    hit_sound.play()
                    walk=1
                    direction=1
                elif event.key == pygame.K_w and player_pos[1] > 0 and player_collide == 0:
                    player_pos[1] -= step + speed_bonus_p1
                    walk_sound.play()
                    walk=1
                elif event.key == pygame.K_w and player_pos[1] > 0 and player_collide == 1:
                    player_pos[1] += step*2
                    cat_pos[1] -= step
                    hit_sound.play()
                    walk=1
                elif event.key == pygame.K_s and player_pos[1] < ((display_height * tile_size) - tile_size) and player_collide == 0:
                    player_pos[1] += step + speed_bonus_p1
                    walk_sound.play()
                    walk=1
                elif event.key == pygame.K_s and player_pos[1] < ((display_height * tile_size) - tile_size) and player_collide == 1:
                    player_pos[1] -= step*2
                    cat_pos[1] += step
                    hit_sound.play()
                    walk=1
                elif event.key == pygame.K_1 and inventory[mush1_tile] >= 5 and inventory[mush1_tile] < 10 and current_tile == 7:
                    # Craft a heart using 5 type-A mushrooms
                    tile_map[0][0] = 8
                    inventory[mush1_tile] = inventory[mush1_tile] - 5
                    craft_sound.play()
                    craft_message("P1 CRAFTED HEART!")
                elif event.key == pygame.K_1 and inventory[mush1_tile] >= 10 and current_tile == 7:
                    # Craft an exit piece 1 using 10 mushrooms
                    tile_map[0][1] = 11
                    orbs_p1 += 1
                    inventory[mush1_tile] = inventory[mush1_tile] - 10
                    craft_sound.play()
                    craft_message("P1 CRAFTED PORTAL PIECE 1!")
                elif event.key == pygame.K_2 and inventory[mush2_tile] >= 5 and inventory[mush2_tile] < 10 and current_tile == 7:
                    # Craft a speed bonus using 5 type-B mushroom
                    tile_map[0][0] = 10
                    inventory[mush2_tile] = inventory[mush2_tile] - 5
                    craft_sound.play()
                    craft_message("P1 CRAFTED SPEED BONUS!")
                elif event.key == pygame.K_2 and inventory[mush2_tile] >= 10 and current_tile == 7:
                    # Craft an exit piece 1 using 10 mushrooms
                    tile_map[1][0] = 11
                    orbs_p1 += 1
                    inventory[mush2_tile] = inventory[mush2_tile] - 10
                    craft_sound.play()
                    craft_message("P1 CRAFTED PORTAL PIECE 2!")
                elif event.key == pygame.K_3 and inventory[mush3_tile] >= 5 and inventory[mush3_tile] < 10 and current_tile == 7:
                    craft_sound.play()
                    craft_message("P1 CRAFTED SPORE MAGIC!")
                    inventory[mush3_tile] = inventory[mush3_tile] - 5
                    spore_magic(tile_map)
                elif event.key == pygame.K_3 and inventory[mush3_tile] >= 10 and current_tile == 7 and orbs_p1 >= 2:
                    # Craft an exit piece 1 using 10 mushrooms
                    tile_map[1][1] = 12
                    inventory[mush3_tile] = inventory[mush3_tile] - 10
                    craft_sound.play()
                    craft_message("P1 CRAFTED PORTAL PIECE 3!")
                                
                # Move cat left
                elif event.key == pygame.K_LEFT and cat_pos[0] > 0 and player_collide == 0:
                    cat_pos[0] -= step + speed_bonus_p2
                    cat_walk_dir=0
                    cat_walking=1
                elif event.key == pygame.K_LEFT and cat_pos[0] > 0 and player_collide == 1:
                    cat_pos[0] += step*2
                    player_pos[0] -= step
                    cat_walk_dir=0
                    cat_walking=1
                    hit_sound.play()
                # Move cat right
                elif event.key == pygame.K_RIGHT and cat_pos[0] < ((display_width * tile_size) - tile_size) and player_collide == 0:
                    cat_pos[0] += step + speed_bonus_p2
                    cat_walk_dir=1
                    cat_walking=1
                elif event.key == pygame.K_RIGHT and cat_pos[0] < ((display_width * tile_size) - tile_size) and player_collide == 1:
                    cat_pos[0] -= step*2
                    player_pos[0] += step
                    cat_walk_dir=1
                    cat_walking=1
                    hit_sound.play()
                # Move cat down
                elif event.key == pygame.K_DOWN and cat_pos[1] < ((display_height * tile_size) - tile_size) and player_collide == 0:
                    cat_pos[1] += step + speed_bonus_p2
                    cat_walking=1
                elif event.key == pygame.K_DOWN and cat_pos[1] < ((display_height * tile_size) - tile_size) and player_collide == 1:
                    cat_pos[1] -= step*2
                    player_pos[1] += step
                    cat_walking=1
                    hit_sound.play()
                # Move cat up
                elif event.key == pygame.K_UP and cat_pos[1] > 0 and player_collide == 0:
                    cat_pos[1] -= step + speed_bonus_p2
                    cat_walking=1
                elif event.key == pygame.K_UP and cat_pos[1] > 0 and player_collide == 1:
                    cat_pos[1] += step*2
                    player_pos[1] -= step
                    cat_walking=1
                    hit_sound.play()
                elif event.key == pygame.K_8 and inventory_cat[mush1_tile] >= 5 and inventory_cat[mush1_tile] < 10 and current_cat_tile == 7:
                    # Craft a heart using 5 mushrooms
                    tile_map[6][8] = 8
                    inventory_cat[mush1_tile] = inventory_cat[mush1_tile] - 5
                    craft_sound.play()
                    craft_message("P2 CRAFTED HEART!")
                elif event.key == pygame.K_8 and inventory_cat[mush1_tile] >= 10 and current_cat_tile == 7:
                    # Craft an Exit Piece 1 using 10 mushrooms
                    orbs_p2+=1
                    tile_map[6][7] = 11
                    inventory_cat[mush1_tile] = inventory_cat[mush1_tile] - 10
                    craft_sound.play()
                    craft_message("P2 CRAFTED PORTAL PIECE 1!")
                elif event.key == pygame.K_9 and inventory_cat[mush2_tile] >= 5 and inventory_cat[mush2_tile] < 10 and current_cat_tile == 7:
                    # Craft a speed bonus using 5 type-B mushroom
                    tile_map[6][8] = 10
                    inventory_cat[mush2_tile] = inventory_cat[mush2_tile] - 5
                    craft_sound.play()
                    craft_message("P2 CRAFTED SPEED BONUS!")
                elif event.key == pygame.K_9 and inventory_cat[mush2_tile] >= 10  and current_cat_tile == 7:
                    # Craft an exit piece 2 using 10 mushrooms
                    orbs_p2+=1
                    tile_map[5][8] = 11
                    inventory_cat[mush2_tile] = inventory_cat[mush2_tile] - 10
                    craft_sound.play()
                    craft_message("P2 CRAFTED PORTAL PIECE 2!")
                elif event.key == pygame.K_0 and inventory_cat[mush3_tile] >= 5 and inventory_cat[mush3_tile] < 10 and current_cat_tile == 7:
                    craft_sound.play()
                    craft_message("P2 CRAFTED SPORE MAGIC!")
                    inventory_cat[mush3_tile] = inventory_cat[mush3_tile] - 5
                    spore_magic(tile_map)
                elif event.key == pygame.K_0 and inventory_cat[mush3_tile] >= 10 and current_cat_tile == 7 and orbs_p2 >= 2:
                    # Craft an exit piece 3 using 10 mushrooms
                    tile_map[5][7] = 12
                    inventory_cat[mush3_tile] = inventory_cat[mush3_tile] - 10
                    craft_sound.play()
                    craft_message("P2 CRAFTED PORTAL PIECE 3!")

            # Check the player locations to make sure they haven't been knocked off the surface
            if player_pos[0] > (display_width * tile_size) - tile_size:
                player_pos[0] = (display_width * tile_size) - tile_size
            elif player_pos[0] < 0:
                player_pos[0] = 0

            if player_pos[1] > (display_height * tile_size) - tile_size:
                player_pos[1] = (display_height * tile_size) - tile_size
            elif player_pos[1] < 0:
                player_pos[1] = 0

            if cat_pos[0] > (display_width * tile_size) - tile_size:
                cat_pos[0] = (display_width * tile_size) - tile_size
            elif cat_pos[0] < 0:
                cat_pos[0] = 0

            if cat_pos[1] > (display_height * tile_size) - tile_size:
                cat_pos[1] = (display_height * tile_size) - tile_size
            elif cat_pos[1] < 0:
                cat_pos[1] = 0            


            # Player 2 tries to eat mushroom if it's on a mushroom tile
            py = math.floor(cat_pos[1]/tile_size)
            px = math.floor(cat_pos[0]/tile_size)
            current_tile = tile_map[py][px]
            if current_tile == 3 or current_tile == 4 or current_tile == 6 or current_tile == 8:
                # Replace with spore tile
                inventory_cat[current_tile] += 1
                tile_map[py][px] = spore_tile
                cat_pickup_sound.play()
                nom=1
            elif current_tile == 9:
                # Poison mushroom, it reduces the player's HP by 1
                p2_dmg = 1
                inventory_cat[heart_tile] -= 1
                nom=1
                tile_map[py][px] = spore_tile
                poison_sound.play()
            elif current_tile == 10:
                # Enable speed bonus
                tile_map[py][px] = blank_tile
                speed_bonus_p2 = step
                speed_count_p2 = 0
                craft_sound.play()
            elif current_tile == 2:
                # Water damage
                p2_dmg = 1
                water_sound.play()
                inventory_cat[mush1_tile] = 0
                inventory_cat[mush2_tile] = 0
                inventory_cat[mush3_tile] = 0
            elif current_tile == 12:
                craft_message("P2 FOUND THE EXIT! +5 POINTS!")
                scorePoint("p2",5)
                game_exit = True
                break

            # Player 1 pick-up mushroom if it's available on current tile
            py = math.floor(player_pos[1]/tile_size)
            px = math.floor(player_pos[0]/tile_size)
            current_tile = tile_map[py][px]
            if current_tile == 3 or current_tile == 4 or current_tile == 6 or current_tile == 8:
                # Add mushroom to inventory
                inventory[current_tile] += 1
                # Replace with spore tile
                tile_map[py][px] = spore_tile
                get_item_sound.play()
            elif current_tile == 9:
                # Player hits a poison mushroom and loses 1 HP
                inventory[heart_tile] -= 1
                tile_map[py][px] = spore_tile
                poison_sound.play()
                p1_dmg = 1
            elif current_tile == 10:
                # Enable speed bonus
                tile_map[py][px] = blank_tile
                speed_bonus_p1 = step
                speed_count_p1 = 0
                craft_sound.play()
            elif current_tile == 2:
                # Water Damage
                p1_dmg = 1
                water_sound.play()
                inventory[mush1_tile] = 0
                inventory[mush2_tile] = 0
                inventory[mush3_tile] = 0
            elif current_tile == 12:
                craft_message("P1 FOUND THE EXIT! +5 POINTS!")
                scorePoint("p1",5)
                game_exit = True
                break

            # If the p1 speed bonus is enabled, set a timer so that it deactivates after 200 ticks
            if speed_count_p1 < 200:
                speed_count_p1 +=1
            elif speed_count_p1 == 200:
                speed_bonus_p1 = 0

            # If the p2 speed bonus is enabled, set a timer so that it deactivates after 200 ticks
            if speed_count_p2 < 200:
                speed_count_p2 +=1
            elif speed_count_p2 == 200:
                speed_bonus_p2 = 0

            # Reset the walking flag for proper walk animation
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    walk=0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
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
                    elif tile_map[row][column] == 7 and frame_count <= 50:
                        game_display.blit(tile_textures[tile_map[row][column]],(column*tile_size,row*tile_size))
                    elif tile_map[row][column] == 7 and frame_count > 50:
                        game_display.blit(camp2_tile,(column*tile_size,row*tile_size))
                    elif tile_map[row][column] == 11 and frame_count > 50:
                        game_display.blit(exitfire2_tile,(column*tile_size,row*tile_size))
                    # Check for wind to animate grass
                    elif tile_map[row][column] == 1 and wind == 1:
                        game_display.blit(grass2_tile,(column*tile_size,row*tile_size))
                    elif tile_map[row][column] == 5:
                        grow_roll = random.randint(0,5000)
                        if grow_roll >= 4998:
                            mush_list = [3,4,6,9]
                            tile_map[row][column] = random.choice(mush_list)
                        game_display.blit(tile_textures[tile_map[row][column]],(column*tile_size,row*tile_size))
                    else:
                        game_display.blit(tile_textures[tile_map[row][column]],(column*tile_size,row*tile_size))

        # Draw the inventory onto the bottom part of the screen
        pygame.draw.rect(game_display,light_cyan,[0,(display_height*tile_size),display_width*tile_size,50])

        place_position = 130
        player_title = inventory_font.render("P1:", True, dark_magenta, light_cyan)
        game_display.blit(player_title, (10,display_height*tile_size+20))
        cpu_title = inventory_font.render("P2:", True, dark_magenta, light_cyan)
        game_display.blit(cpu_title, (460,display_height*tile_size+20))

        for item in resources:
            game_display.blit(tile_textures[item], (place_position-90, display_height*tile_size-20))
            place_position += 1
            text_object = inventory_font.render(str(inventory[item]),True,magenta,light_cyan)
            game_display.blit(text_object, (place_position-20,display_height*tile_size+20))

            game_display.blit(tile_textures[item], (place_position+360, display_height*tile_size-20))
            place_position += 1
            text_object = inventory_font.render(str(inventory_cat[item]),True, magenta,light_cyan)
            game_display.blit(text_object, (place_position+430,display_height*tile_size+20))

            place_position += 80

        # Animate cat when it eats mushroom
        if nom >= 1:
            nom+=1
        if nom > 20:
            nom=0

        #Animate cat walk
        if cat_walking >= 1:
            cat_walking+=1
        if cat_walking > 10:
            cat_walking=0

        # Render the cat sprite depending on direction and current action
        if p2_dmg == 1 and cat_walk_dir == 0:
            game_display.blit(cat_dmg_flip,(cat_pos[0],cat_pos[1]))
        elif p2_dmg == 1 and cat_walk_dir == 1:
            game_display.blit(cat_dmg,(cat_pos[0],cat_pos[1]))
        elif cat_walk_dir == 0 and nom == 0 and cat_walking == 0:
            game_display.blit(cat_main,(cat_pos[0],cat_pos[1]))
        elif cat_walk_dir == 0 and nom == 0 and cat_walking >= 1:
            game_display.blit(cat_walk,(cat_pos[0],cat_pos[1]))
        elif cat_walk_dir == 1 and nom == 0 and cat_walking == 0:
            game_display.blit(cat_main_flip,(cat_pos[0],cat_pos[1]))
        elif cat_walk_dir == 1 and nom == 0 and cat_walking >= 1:
            game_display.blit(cat_walk_flip,(cat_pos[0],cat_pos[1]))
        elif cat_walk_dir == 0 and nom >= 1:
            game_display.blit(cat_eat,(cat_pos[0],cat_pos[1]))
        elif cat_walk_dir == 1 and nom >= 1:
            game_display.blit(cat_eat_flip,(cat_pos[0],cat_pos[1]))

        # Render the player character
        if p1_dmg == 1 and direction == 0:
            game_display.blit(player_dmg,(player_pos[0],player_pos[1]))
        elif p1_dmg == 1 and direction == 1:
            game_display.blit(player_dmg_flip,(player_pos[0],player_pos[1]))
        elif walk == 0 and direction == 0:
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
            p1_dmg = 0
            p2_dmg = 0
        wind_roll = random.randint(0,40)
        if wind_roll > 39:
            wind = 0

        # Check the player's health, if it's game over reset the inventory 
        if inventory[heart_tile] < 1:
            craft_message("P1 LOST BY POISON!")
            game_exit = True
            scorePoint("p2",1)

        # Check the cat's health, game over/reset if it's zero
        if inventory_cat[heart_tile] < 1:
            craft_message("P2 LOST BY POISON!")
            game_exit = True
            scorePoint("p1",1)


main_menu()

while True:
    game_loop()
    game_over()

pygame.quit()
quit()

import pygame
import os
import random

pygame.init()

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#TILESIZE = 32
#MAPWIDTH = 30
#MAPHEIGHT = 20
light_cyan = (85,255,255)
dark_cyan = (0,170,170)
dark_green = (0,170,0)
light_green = (85,255,85)

display_width = 864
display_height = 672

game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Dark Magenta')

time_passed = 0
clock = pygame.time.Clock()

# Load in sprites
player = pygame.image.load(os.path.join(__location__,'magenta_start.png'))
player_walk = pygame.image.load(os.path.join(__location__,'magenta_walk.png'))
coolcat1 = pygame.image.load(os.path.join(__location__,'cat1.png'))
coolcat2 = pygame.image.load(os.path.join(__location__,'cat2.png'))
grass1 = pygame.image.load(os.path.join(__location__,'grass1.png'))
grass2 = pygame.image.load(os.path.join(__location__,'grass2.png'))
mushroom1 = pygame.image.load(os.path.join(__location__,'mush1.png'))
pond1 = pygame.image.load(os.path.join(__location__,'pond1.png'))
pond2 = pygame.image.load(os.path.join(__location__,'pond2.png'))

# Load in sound effects
walk_sound = pygame.mixer.Sound(os.path.join(__location__,'sound_walk.wav'))
walk_sound.set_volume(0.5)

# Play a little song to start the level
intro_tune = pygame.mixer.Sound(os.path.join(__location__,'bgmusic1.mp3'))
intro_tune.set_volume(0.4)
intro_tune.play(0,0,8000)

# Repeat ambient background sounds
pygame.mixer.music.load(os.path.join(__location__, "forestsounds.mp3"))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1,8000)

player_size = 96
grass_size = 96

def draw_player(x,y,walk):
    if walk == 1:
        game_display.blit(player_walk,(x,y))
    else:
        game_display.blit(player,(x,y))

def draw_pond(x,y,wind):
    if wind == 1:
        game_display.blit(pond1,(x,y))
    else:
        game_display.blit(pond2,(x,y))  

def draw_grass(x,y,wind):
    if wind == 1:
        game_display.blit(grass2,(x,y))
    else:
        game_display.blit(grass1,(x,y))

def draw_mushroom(x,y):
    game_display.blit(mushroom1,(x,y))

def draw_cat(x,y,wind):
    if wind == 1:
        game_display.blit(coolcat1, (x,y))
    else:
        game_display.blit(coolcat2, (x,y))

def generate_terrain():
    # Blank tile = 0
    # Grass tile = 1
    # Mushroom #1 = 2
    # Pond = 3

    terrain_tiles=[]
    row_list = []
    
    col=0
    while col < 9:
        i=0
        while i < 7:
            # Grass tile roll
            grass_roll = random.randint(0,1)
            row_list.append(grass_roll)

            # Mushroom tile roll
            mush_roll = random.randint(0,10)
            if mush_roll > 8:
                row_list.append(2)
            else:
                pond_roll = random.randint(0,20)
                if pond_roll > 19:
                    row_list.append(3)

            i+=1
        terrain_tiles.append(row_list)
        row_list=[]
        col+=1
        # Hack to keep the first two tiles clear
    terrain_tiles[0][0] = 0
    terrain_tiles[1][0] = 0

    return terrain_tiles

def place_generated_tiles(terrain_tiles,wind):
        c=0
        r=0
        for row in terrain_tiles:
            for cell in row:
                if cell == 1:
                    draw_grass(c,r,wind)
                elif cell == 2:
                    draw_grass(c,r,wind)
                    draw_mushroom(c,r)
                elif cell == 3:
                    draw_pond(c,r,wind)
                r+=96
            c+=96
            r=0    

def game_loop():

    x = 0
    y = 0
    x_change = 0
    y_change = 0
    walked=0
    wind=0
    time_passed = 0
    
    terrain_tiles = generate_terrain()

    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                elif event.key == pygame.K_RIGHT:
                    x_change = 10
                if event.key == pygame.K_UP:
                    y_change = -10
                elif event.key == pygame.K_DOWN:
                    y_change = 10

                walked=1
                walk_sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

                walked=0

            # Apply X and Y movement to the player
            x+=x_change
            y+=y_change

        game_display.fill(dark_cyan)

        dt = clock.tick()
        time_passed += dt
        if time_passed >= 30 and time_passed < 60:
            wind=1
        elif time_passed >= 60:
            wind=0
            time_passed = 0

        # Draw sprites onto surface
        place_generated_tiles(terrain_tiles,wind)
        draw_cat(96,0,wind)
        draw_player(x,y,walked)

        pygame.display.update()

        clock.tick(60)

game_loop()
pygame.quit()
quit()
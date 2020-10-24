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
clock = pygame.time.Clock()

# Load in sprites
player = pygame.image.load(os.path.join(__location__,'magenta_start.png'))
player_walk = pygame.image.load(os.path.join(__location__,'magenta_walk.png'))
grass = pygame.image.load(os.path.join(__location__,'grass1.png'))
mushroom1 = pygame.image.load(os.path.join(__location__,'mush1.png'))

player_size = 96
grass_size = 96

def draw_player(x,y,walk):
    if walk == 1:
        game_display.blit(player_walk,(x,y))
    else:
        game_display.blit(player,(x,y))

def draw_grass(x,y):
    game_display.blit(grass,(x,y))

def draw_mushroom(x,y):
    game_display.blit(mushroom1,(x,y))

def generate_terrain():
    # Blank tile = 0
    # Grass tile = 1
    # Mushroom #1 = 2
    # Mushroom #2 = 3
    # Mushroom #3 = 4
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

            i+=1
        terrain_tiles.append(row_list)
        row_list=[]
        col+=1

    return terrain_tiles

def place_generated_tiles(terrain_tiles):
        c=0
        r=0
        for row in terrain_tiles:
            for cell in row:
                if cell == 1:
                    draw_grass(c,r)
                elif cell == 2:
                    draw_grass(c,r)
                    draw_mushroom(c,r)
                    pass
                r+=96
            c+=96
            r=0    

def game_loop():

    x = 64
    y = 64
    x_change = 0
    y_change = 0
    walked=0
    
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

        place_generated_tiles(terrain_tiles)
        draw_player(x,y,walked)

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
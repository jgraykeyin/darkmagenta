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

player = pygame.image.load(os.path.join(__location__,'magenta_start.png'))
grass = pygame.image.load(os.path.join(__location__,'grass_one.png'))

player_size = 96
grass_size = 96

def draw_player(x,y):
    game_display.blit(player,(x,y))

def draw_grass(x,y):
    game_display.blit(grass,(x,y))

def generate_grass():
    grass_placement=[]
    row_list = []
    
    col=0
    while col < 9:
        i=0
        while i < 9:
            row_list.append(random.randint(0,1))
            i+=1
        grass_placement.append(row_list)
        row_list=[]
        col+=1

    return grass_placement

def place_generated_grass(grass_placement):
        c=0
        r=0
        for row in grass_placement:
            for cell in row:
                if cell == 1:
                    draw_grass(c,r)
                r+=96
            c+=96
            r=0    

def game_loop():

    x = 64
    y = 64
    x_change = 0
    
    grass_placement = generate_grass()

    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -4
                elif event.key == pygame.K_RIGHT:
                    x_change = 4

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

            # Apply X movement to the plauyer
            x+=x_change

        game_display.fill(dark_cyan)

        place_generated_grass(grass_placement)
        draw_player(x,y)

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
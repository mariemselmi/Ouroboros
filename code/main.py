import pygame, sys
from level import Level
from game_data import csv
pygame.init()

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
level = Level(csv,screen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    #the whole game run
    level.run()


    pygame.display.update()
    clock.tick(60)



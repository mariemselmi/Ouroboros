import pygame
from support import import_csv_layout
from tiles import Tile 

class Level: 
    def __init__(self,level_data,surface):
        self.display_surface = surface

        background = import_csv_layout(level_data['green1']) 
        self.terrain_sprites = self.create_tile_group(background,'green1')
    
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):


                if val != '-1':
                    x= col_index*64#tilesize
                    y= row_index*64

                    if type == 'green1':
                        sprite = Tile(64,x,y)
                        sprite_group.add(sprite)
        return sprite_group

    def run(self):
        self.terrain_sprites.draw(self.display_surface)

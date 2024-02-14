import pygame

class Sword:
    def __init__(self,name,decription,image,damage):
        self.name = name
        self.decription = decription
        self.image = pygame.image.load(image).convert_alpha()
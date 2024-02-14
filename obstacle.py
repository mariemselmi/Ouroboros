import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image,scale):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

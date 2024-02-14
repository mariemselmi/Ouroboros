import pygame


class Button():
    def __init__(self, x, y, unpushed_image, pushed_image, scale):
        self.unpushed_image = pygame.transform.scale(unpushed_image, (int(unpushed_image.get_width() * scale), int(unpushed_image.get_height() * scale))).convert_alpha()
        self.pushed_image = pygame.transform.scale(pushed_image, (int(pushed_image.get_width() * scale), int(pushed_image.get_height() * scale))).convert_alpha()
        self.image = self.unpushed_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.is_pressed:
                self.is_pressed = True
                self.image = self.pushed_image
            elif pygame.mouse.get_pressed()[0] == 0 and self.is_pressed:
                action = True
                self.is_pressed = False
                self.image = self.unpushed_image
        else:
            self.is_pressed = False
            self.image = self.unpushed_image

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

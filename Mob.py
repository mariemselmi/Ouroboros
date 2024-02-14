import random
import pygame
class Mob:
    def __init__(self, x, y, image,max_health, speed, scale):
        self.image = pygame.transform.scale(image, (
        int(image.get_width() * scale), int(image.get_height() * scale))).convert_alpha()
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.max_health = max_health
        self.health = max_health
        self.state = 'wander'
        self.move_counter = 0
        self.idle_counter = 0
        self.move_direction = random.choice(['up', 'down', 'left', 'right'])

    def wander(self):
        if self.move_counter < 50:
            # Move in the chosen direction
            move_distance = random.randint(1, 2)
            if self.move_direction == 'up' and self.rect.y - self.speed > 0:
                self.rect.y -= self.speed
            elif self.move_direction == 'down' and self.rect.y + self.speed < 620 - self.rect.height:
                self.rect.y += self.speed
            elif self.move_direction == 'left' and self.rect.x - self.speed > 0:
                self.rect.x -= self.speed
            elif self.move_direction == 'right' and self.rect.x + self.speed < 1040 - self.rect.width:
                self.rect.x += self.speed

            self.move_counter += 1
        else:
            # Pause for a certain number of iterations
            if self.idle_counter < 30:
                self.idle_counter += 1
            else:
                # Reset counters and choose a new direction
                self.move_counter = 0
                self.idle_counter = 0
                self.move_direction = random.choice(['up', 'down', 'left', 'right'])
    def take_damage(self,damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def update(self):
        if self.state == 'wander':
            self.wander()


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def draw_health_bar(self, surface):
        health_bar_length = 50
        health_ratio = self.health / self.max_health
        health_bar_width = int(health_bar_length * health_ratio)
        health_bar_color = (255,0,0)  # Green for healthy
        pygame.draw.rect(surface, health_bar_color, (self.rect.x, self.rect.y - 10, health_bar_width, 5))

    def is_alive(self):
        return self.health > 0
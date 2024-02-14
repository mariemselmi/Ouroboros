import pygame
pygame.mixer.init()
hurt_sound=pygame.mixer.Sound('take_damage.mp3')
class Character:
    def __init__(self,x,y,speed,max_health,image,scale):
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.vect=pygame.math.Vector2(0,0)
        self.max_health = max_health
        self.health = max_health
        self.immunity = False
        self.immunity_event = pygame.USEREVENT + 1
        self.facing = "right"
        self.swinging = False
        self.swing_timer = 0
        self.swing_duration = 30

    def move(self, keys,obstacles):

        # Handle character movement based on pressed keys
        if keys[pygame.K_LEFT]:
            self.vect.x = -self.speed
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            self.vect.x = self.speed
            self.facing = "right"
        if keys[pygame.K_UP]:
            self.vect.y = -self.speed
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            self.vect.y = self.speed
            self.facing = "down"

        # Move the character rect by the calculated movement vector
        self.rect.x += self.vect.x
        self.rect.y += self.vect.y

        # Check for collision with obstacles
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # If collision detected, move character back to previous position
                self.rect.x -= self.vect.x
                self.rect.y -= self.vect.y



    def take_damage(self,enemies,damage):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if not self.immunity:
                    self.immunity = True
                    self.health -= damage
                    hurt_sound.play()
                    pygame.time.set_timer(self.immunity_event,1000)
                    if self.health <= 0:
                        self.health = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_health_bar(self, surface):
        health_bar_length = 50
        health_ratio = self.health / self.max_health
        health_bar_width = int(health_bar_length * health_ratio)
        health_bar_color = (0, 255, 0)  # Green for healthy
        pygame.draw.rect(surface, health_bar_color, (self.rect.x, self.rect.y - 10, health_bar_width, 5))


    def draw_and_get_sword_rect(self, screen, sword_image):
        # Define sword dimensions relative to character size
        sword_width = int(self.rect.width * 0.7)
        sword_height = int(self.rect.height * 0.7)

        if self.facing == 'left':
            # Position sword to the left of the character
            sword_pos = (self.rect.left - sword_width, self.rect.centery - sword_height / 2)
        elif self.facing == 'right':
            # Position sword to the right of the character
            sword_pos = (self.rect.right, self.rect.centery - sword_height / 2)
        elif self.facing == 'up':
            # Position sword above the character
            sword_pos = (self.rect.centerx - sword_width / 2, self.rect.top - sword_height)
        elif self.facing == 'down':
            # Position sword below the character
            sword_pos = (self.rect.centerx - sword_width / 2, self.rect.bottom)

        # Resize the sword image to match the calculated dimensions
        sword_image = pygame.transform.scale(sword_image, (sword_width, sword_height))

        # Draw the sword image on the screen
        screen.blit(sword_image, sword_pos)

        # Create and return the rectangle object for the sword
        return pygame.Rect(sword_pos, (sword_width, sword_height))
#manages the groups of mobs
import pygame
import random
from config import SCREEN_WIDTH,SCREEN_HEIGHT
from Mob import Mob
ENEMY_SPAWN_INTERVAL = 5000  # Interval between enemy waves in milliseconds
pygame.init()
pixel_font = pygame.font.Font("VCR_OSD_MONO_1.001.ttf",40)
class Timer:
    def __init__(self):
        self.font = pixel_font
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.elapsed_time = pygame.time.get_ticks() - self.start_time

    def draw(self, screen):
        minutes = int(self.elapsed_time // 60000)  # Convert milliseconds to minutes
        seconds = int((self.elapsed_time % 60000) // 1000)  # Convert remaining milliseconds to seconds
        text = "Time: {:02d}:{:02d}".format(minutes, seconds)  # Format minutes and seconds
        timer_surface = self.font.render(text, True, (255, 255, 255))
        text_width = timer_surface.get_width()
        x_position = (SCREEN_WIDTH - text_width) // 2
        screen.blit(timer_surface, (x_position, 10))
class Wave:
    def __init__(self, wave_number, num_enemies, max_health):
        self.wave_number = wave_number
        self.num_enemies = num_enemies
        self.max_health = max_health
class Enemy_Manager:
    def __init__(self):
        self.enemies = []
        self.current_wave = 0
        self.spawn_timer = 0
        self.enemy_spawn_interval = ENEMY_SPAWN_INTERVAL
        self.waves = [
            Wave(1, 6, 10),
            Wave(2, 6, 15),
            Wave(3, 6, 20),
            # Add more waves with increasing difficulty
        ]
        self.spawn_new_wave = True  # Flag to control spawning of new waves
        self.total_waves = len(self.waves)  # Total number of waves

    def update(self, enemy_image, speed, scale):
        # Spawn new wave if no enemies remaining and there are more waves
        if not self.enemies and self.current_wave < self.total_waves and self.spawn_new_wave:
            self.spawn_wave(enemy_image, speed, scale)
            self.spawn_new_wave = False

        # Spawn enemies based on timer
        self.spawn_timer += pygame.time.get_ticks()
        if self.spawn_timer >= self.enemy_spawn_interval:
            self.spawn_timer = 0
            self.spawn_new_wave = True  # Allow spawning of next wave

        # Update enemies
        for enemy in self.enemies:
            enemy.update()


    def spawn_wave(self, enemy_image, speed, scale):
        if self.current_wave < len(self.waves):
            wave = self.waves[self.current_wave]
            for _ in range(wave.num_enemies):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                new_enemy = Mob(x, y, enemy_image, wave.max_health, speed, scale)
                self.enemies.append(new_enemy)
            self.current_wave += 1

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
            enemy.draw_health_bar(screen)

    def check_collisions(self, character, sword_rect):
        for enemy in self.enemies:
            if sword_rect.colliderect(enemy.rect):
                print("collision")
                enemy.take_damage(2)

    def remove_dead_enemies(self):
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive()]
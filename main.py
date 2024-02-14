from turtle import width

import pygame
import math
import Button
import Character
import Mob
import random
from obstacle import Obstacle

from Enemy_Manager import *
from config import SCREEN_WIDTH, SCREEN_HEIGHT,FPS

####CAPITAL LETTER VARIABLE NAMES ==> CONSTANTS####

class GameState:
    MENU = 'menu'
    GAME = 'game'
    GAME_OVER = 'game_over'
    GAME_OVER_SUCCESS = 'game_over_success'
    GAME_OVER_TIMER = 'game_over_timer'

def character_animation_method(keys,FRAME_CHANGE):
        ###BASIC MOVEMENT###
        global character_index, character_image, character_direction
        if keys[pygame.K_DOWN] ==True:
            character_direction=0
            character_index+=FRAME_CHANGE
            if int(character_index)>= len(character_anim[0]):
                character_index=1

        elif keys[pygame.K_UP]:
            character_direction=1
            character_index+=FRAME_CHANGE
            if int(character_index)>= len(character_anim[0]):
                character_index=1

        elif keys[pygame.K_LEFT]:
            character_direction=2
            character_index+=FRAME_CHANGE
            if int(character_index)>= len(character_anim[0]):
                character_index=1

        elif keys[pygame.K_RIGHT]:
            character_direction=3
            character_index+=FRAME_CHANGE
            if int(character_index)>= len(character_anim[0]):
                character_index=1

        ### OTHER ANIMATIONS (TEST) ###
        character_image=character_anim[character_direction][int(character_index)]

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen = pygame.display.get_surface()



pygame.display.set_caption("Ouroboros")
icon = pygame.image.load("Ouroboros.svg.png")
pixel_font = pygame.font.Font("VCR_OSD_MONO_1.001.ttf",65)

bg = pygame.image.load("Menu-Pictures/menu1.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()


##CONSTANT LISTS FOR ANIMATION##
CHARACTER_RESTDOWN=pygame.image.load("Test-Character/atRestDOWN.png").convert_alpha()
CHARACTER_MOVE1DOWN=pygame.image.load("Test-Character/movingFrame1DOWN.png").convert_alpha()
CHARACTER_MOVE2DOWN=pygame.image.load("Test-Character/movingFrame2DOWN.png").convert_alpha()

CHARACTER_RESTUP=pygame.image.load("Test-Character/atRestUP.png").convert_alpha()
CHARACTER_MOVE1UP=pygame.image.load("Test-Character/movingFrame1UP.png").convert_alpha()
CHARACTER_MOVE2UP=pygame.image.load("Test-Character/movingFrame2UP.png").convert_alpha()

CHARACTER_RESTRIGHT=pygame.image.load("Test-Character/atRestRIGHT.png").convert_alpha()
CHARACTER_MOVE1RIGHT=pygame.image.load("Test-Character/movingFrame1RIGHT.png").convert_alpha()
CHARACTER_MOVE2RIGHT=pygame.image.load("Test-Character/movingFrame2RIGHT.png").convert_alpha()

CHARACTER_RESTLEFT=pygame.image.load("Test-Character/atRestLEFT.png").convert_alpha()
CHARACTER_MOVE1LEFT=pygame.image.load("Test-Character/movingFrame1LEFT.png").convert_alpha()
CHARACTER_MOVE2LEFT=pygame.image.load("Test-Character/movingFrame2LEFT.png").convert_alpha()

CHARACTER_CHANGE=pygame.image.load("character.png").convert_alpha()
sword_image = pygame.image.load("sword.png").convert_alpha()

character_anim=[[CHARACTER_RESTDOWN, CHARACTER_MOVE1DOWN, CHARACTER_MOVE2DOWN],
                [CHARACTER_RESTUP, CHARACTER_MOVE1UP, CHARACTER_MOVE2UP],
                [CHARACTER_RESTLEFT, CHARACTER_MOVE1LEFT, CHARACTER_MOVE2LEFT],
                [CHARACTER_RESTRIGHT, CHARACTER_MOVE1RIGHT, CHARACTER_MOVE2RIGHT]]
FRAME_CHANGE=0.08
character_index=0
character_direction=0



pygame.display.set_icon(icon)
# Load images
unpushed_start_image = pygame.image.load("Menu-Pictures/play-export.png")
pushed_start_image = pygame.image.load("Menu-Pictures/play-export.png") ##IN NEED OF CHANGE
unpushed_quit_image = pygame.image.load("Menu-Pictures/quit-export.png")
pushed_quit_image = pygame.image.load("Menu-Pictures/quit-export.png") ##IN NEED OF CHANGE
character_image = character_anim[character_direction][character_index]
heart_image = pygame.image.load("heart.png")
floor_image = pygame.image.load("floor.png")
heart_image = pygame.transform.scale(heart_image, (20, 20))
mob_image = pygame.image.load("mob.png")
rock = pygame.image.load("7jar.png")
start_button = Button.Button(145, 130, unpushed_start_image, pushed_start_image, 0.85)
quit_button = Button.Button(665, 130, unpushed_quit_image, pushed_quit_image, 0.83)
character_scale=0.2
character = Character.Character(60, 40, 3, 10,character_image,character_scale)
current_game_state = GameState.MENU
enemy_manager = Enemy_Manager()
num_obstacles = 6
obstacles = []

for _ in range(num_obstacles):
    # Random positions for each obstacle
    obstacle_x = random.randint(0, SCREEN_WIDTH - rock.get_width())
    obstacle_y = random.randint(0, SCREEN_HEIGHT - rock.get_height())
    # Create obstacle object and add it to the list
    obstacles.append(Obstacle(obstacle_x, obstacle_y, rock, 1))


### SAMPLE MUSIC ###
intro=pygame.mixer.Sound('Music/intro-music.mp3')
running_music=pygame.mixer.Sound('Music/running.wav')
swing_sound=pygame.mixer.Sound('sword_slash.mp3')
scaled_floor = pygame.transform.scale(floor_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
timer = Timer()

space_pressed = False
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if current_game_state == GameState.MENU:
        screen.blit(pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        action1 = start_button.draw(screen)
        action2 = quit_button.draw(screen)
        if action1:
            current_game_state = GameState.GAME
        if action2:
            running = False
    elif current_game_state == GameState.GAME:
        intro.stop()
        screen.blit(scaled_floor, (0, 0))
        for obstacle in obstacles:
            obstacle.draw(screen)
        elapsed_time = pygame.time.get_ticks() - timer.start_time  # Calculate elapsed time
        if elapsed_time >= 60000:  # If one minute (60000 milliseconds) has passed
            current_game_state = GameState.GAME_OVER_TIMER
        character.move(keys,obstacles)
        character_animation_method(keys, FRAME_CHANGE)
        character.draw(screen)

        if enemy_manager.current_wave >= enemy_manager.total_waves and not enemy_manager.enemies:
            # Transition to "Game Over" state with congratulatory message
            current_game_state = GameState.GAME_OVER_SUCCESS
        # Update enemy manager
        enemy_manager.update(mob_image, 1, 0.1)

        # Check if all enemies are defeated
        if len(enemy_manager.enemies) == 0:
            # Spawn new wave if no enemies remaining
            enemy_manager.spawn_wave(mob_image, 1, 0.1)

        timer.update()
        enemy_manager.draw_enemies(screen)
        timer.draw(screen)
        character.take_damage(enemy_manager.enemies, 1)
        enemy_manager.remove_dead_enemies()

        character.image = pygame.transform.scale(character_image, (int(character_image.get_width() * character_scale),
                                                                   int(character_image.get_height() * character_scale))).convert_alpha()
        character.draw(screen)
        character.draw_health_bar(screen)
        if character.swinging:
            swing_sound.play()
            sword_rect = character.draw_and_get_sword_rect(screen, sword_image)
            enemy_manager.check_collisions(character, sword_rect)
            character.swinging = False
        if character.health <= 0:
            current_game_state = GameState.GAME_OVER
        heart_spacing = 25
        for i in range(character.health):
            screen.blit(heart_image, (10 + i * heart_spacing, 10))

    elif current_game_state == GameState.GAME_OVER:
        # Display "You Died" message on a black screen
        screen.fill((0, 0, 0))
        text = pixel_font.render("You Died", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
    elif current_game_state == GameState.GAME_OVER_SUCCESS:
        # Display congratulatory message
        screen.fill((0, 0, 0))

        # Create a smaller font size for the message
        text = pixel_font.render("Good job adventurer!", True, (255, 255, 255))
        text2 = pixel_font.render("You kept the minions from spreading their diseases.", True, (255, 255, 255))

        # Calculate the positions for the two lines of text
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

        # Blit the text onto the screen
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
    elif current_game_state == GameState.GAME_OVER_TIMER:
        # Display game over message due to timer expiration
        screen.fill((0, 0, 0))

        # Create a smaller font size for the message
        text = pixel_font.render("This area has been corrupted", True, (255, 255, 255))
        text2 = pixel_font.render("By the minions' deceases.", True, (255, 255, 255))

        # Calculate the positions for the two lines of text
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

        # Blit the text onto the screen
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)

    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            running = False
        if current_game_state == GameState.GAME and event.type == character.immunity_event:
            character.immunity = False
        if event.type==pygame.KEYUP:
            character.vect.x=0
            character.vect.y=0
            character_index=0
            character_image=character_anim[character_direction][int(character_index)]
            character.image=pygame.transform.scale(character_image, (int(character_image.get_width() * character_scale), int(character_image.get_height() * character_scale))).convert_alpha()
            running_music.stop()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                running_music.play()
            if event.key == pygame.K_SPACE:
                space_pressed = True
                character.swinging = True



    pygame.display.update()
    pygame.display.flip()

pygame.quit()
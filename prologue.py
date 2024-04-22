import pygame
import sys
import time

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Ouroboros")

# Font settings
font = pygame.font.Font("font/font.ttf", 25)
texts = [
    "Long ago, a war broke between the people of Eldoria and the wicked king Ophiuchus.",
    "The villagers fought fiercely and endured for their freedom...",
    "until finally...", "Eldoria emerged victorious!",
    "However, fueled by vengeance even in his dying breath..", 
    "the malevolent king unleashed a curse that would linger for over a century",
    "A few years later..",
    "Fifth text example.",
    "Last text to display in the sequence."
]

# Images
images = [
    pygame.image.load('graphics/prologue/2.1.png').convert_alpha(),
    pygame.image.load('graphics/prologue/1.1.jpg').convert_alpha(),
    pygame.image.load('graphics/prologue/2.png').convert_alpha(),
    pygame.image.load('graphics/prologue/2.png').convert_alpha(),
    pygame.image.load('graphics/prologue/3.jpg').convert_alpha(),
    pygame.image.load('graphics/prologue/3.jpg').convert_alpha(),
    pygame.image.load('graphics/prologue/2.1.png').convert_alpha(),
    pygame.image.load('graphics/prologue/2.1.png').convert_alpha(),
    pygame.image.load('graphics/prologue/2.1.png').convert_alpha()
]
for i in range(len(images)):
    images[i] = pygame.transform.scale(images[i], (760, 475))  # Adjust size as needed

# Typewriter effect variables
typing_speed = 0.08  # Adjust typing speed (lower value = faster typing)

clock = pygame.time.Clock()
running = True

text_index = 0
typing_complete = False
image_index = 0
show_image = True  # Flag to track whether to show the image

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(BLACK)

    # Display the image and text simultaneously
    
    if show_image:
        screen.blit(images[image_index], (430, 220))

    # Typewriter effect for the current text
    if not typing_complete:
        if text_index < len(texts[image_index]):
            text_surface = font.render(texts[image_index][:text_index + 1], True, WHITE)
            text_index += 1
        else:
            typing_complete = True

        text_rect = text_surface.get_rect(center=(WIDTH , HEIGHT +155))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

    time.sleep(typing_speed)

    # Move to the next text and image
    if typing_complete:
        time.sleep(0.78)  # Pause for 1 second after displaying each text
        text_index = 0
        typing_complete = False
        image_index += 1
        show_image = True  # Show the next image
        if image_index >= len(texts):  # Stop when all texts are displayed
            running = False

pygame.quit()
sys.exit()

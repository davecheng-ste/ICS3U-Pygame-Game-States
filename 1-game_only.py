"""
Author: D. Cheng
Date: 2024-06-06
Description: Pygame ocean tech demo with collisions and score.
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Ocean")

# Define constant colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize game conditions
player_score = 0

# Load text surfaces and initialize text Rect
font_instructions = pygame.font.Font(None, 18)  # None uses the default system font, 12 size
text_instructions_string = "WASD to move shark. Catch as many shrimp as you can!"
text_instructions_surface = font_instructions.render(text_instructions_string, True, WHITE)  # Render text onto a surface
text_instructions_rect = text_instructions_surface.get_rect(center=(WIDTH // 2, HEIGHT - 10))  # Position text at the bottom center

font_score = pygame.font.Font(None, 32)
text_score_string = f"Score: {player_score}"
text_score_surface = font_score.render(text_score_string, True, WHITE)
text_score_rect = text_score_surface.get_rect()
text_score_rect.x, text_score_rect.y = 10, 10

# Load static background image
ocean_background = pygame.image.load("images/water_background.png")
ocean_background = pygame.transform.scale(ocean_background, (WIDTH, HEIGHT))

# Load shrimp sprite and initialize Rect
shrimp = pygame.image.load("images/shrimp.png")
shrimp_rect = shrimp.get_rect()
shrimp_rect.left = WIDTH
shrimp_rect.centery = 100
shrimp_speed = 10

# Load shark sprites into a list
shark_frames = [
    pygame.image.load("images/shark01.png"),
    pygame.image.load("images/shark02.png")
]

# Define Rect object to move and blit shark sprites
shark_rect = shark_frames[0].get_rect()
shark_rect.centerx = WIDTH // 2
shark_rect.centery = HEIGHT // 2
shark_speed = 8

# Set up animation frame refresh mechanism
shark_frame_duration = 250  # Frame duration in millseconds (ms)
shark_frame_index = 0  # List index to be used with shark_frames
shark_time_changed = pygame.time.get_ticks()

clock = pygame.time.Clock()  # Create a Clock object for controlling frame rate

# Define main game loop

running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Handle key presses
    keys = pygame.key.get_pressed()

    # Handle shark movement key presses
    if keys[pygame.K_w] and shark_rect.top >= 0:
        shark_rect.y -= shark_speed
    elif keys[pygame.K_s] and shark_rect.bottom <= HEIGHT:
        shark_rect.y += shark_speed
    if keys[pygame.K_d] and shark_rect.right <= WIDTH:
        shark_rect.x += shark_speed
    elif keys[pygame.K_a] and shark_rect.left >= 0:
        shark_rect.x -= shark_speed

    # Handle shrimp movement
    if shrimp_rect.right >= 0 :
        shrimp_rect.x -= shrimp_speed  # Move shrimp left
    else:
        shrimp_rect.left = WIDTH 
        shrimp_rect.centery = random.randint(20, HEIGHT - 20)  # Regenerate shrimp

    # Handle shark and shrimp collisions
    if shark_rect.colliderect(shrimp_rect):
        shrimp_rect.left = WIDTH
        shrimp_rect.centery = random.randint(20, HEIGHT - 20)
        # Increase score and rerender text surface
        player_score += 1
        text_score_string = f"Score: {player_score}"
        text_score_surface = font_score.render(text_score_string, True, WHITE)

    # Update sprite animation frames
    time_now = pygame.time.get_ticks()
    if time_now - shark_time_changed > shark_frame_duration:
        if shark_frame_index == (len(shark_frames) - 1):
            shark_frame_index = 0
        else:
            shark_frame_index += 1
        shark_time_changed = time_now
    
    # Draw graphics
    screen.blit(ocean_background, (0, 0))
    screen.blit(shark_frames[shark_frame_index], shark_rect)
    screen.blit(shrimp, shrimp_rect)
    screen.blit(text_instructions_surface, text_instructions_rect)
    screen.blit(text_score_surface, text_score_rect)
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame   
pygame.quit()
sys.exit()

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

# Game states
OPENING = 0
PLAYING = 1
GAME_OVER = 2

# Initialize game conditions
player_score = 0
game_state = OPENING

# Load text surfaces and initialize text Rect
font_instructions = pygame.font.Font(None, 36)
text_instructions_string = "Press SPACE to start"
text_instructions_surface = font_instructions.render(text_instructions_string, True, WHITE)
text_instructions_rect = text_instructions_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

font_instructions_details = pygame.font.Font(None, 24)
text_instructions_details_string = "WASD to move shark. Can you catch 5 shrimp?"
text_instructions_details_surface = font_instructions_details.render(text_instructions_details_string, True, WHITE)
text_instructions_details_rect = text_instructions_details_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

font_score = pygame.font.Font(None, 32)
text_score_string = f"Score: {player_score}"
text_score_surface = font_score.render(text_score_string, True, WHITE)
text_score_rect = text_score_surface.get_rect()
text_score_rect.x, text_score_rect.y = 10, 10

font_game_over = pygame.font.Font(None, 48)
text_game_over_string = "Game Over! Press SPACE to retry."
text_game_over_surface = font_game_over.render(text_game_over_string, True, WHITE)
text_game_over_rect = text_game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

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
shark_frame_duration = 250  # Frame duration in milliseconds (ms)
shark_frame_index = 0  # List index to be used with shark_frames
shark_time_changed = pygame.time.get_ticks()

clock = pygame.time.Clock()  # Create a Clock object for controlling frame rate


def handle_events():
    """
    Handles all Pygame events such as quitting the game and key presses.

    Returns:
        bool: False if the game should quit, True otherwise.
    """
    global game_state, player_score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE:
                if game_state == OPENING or game_state == GAME_OVER:
                    start_game()
    return True


def start_game():
    """
    Starts the game by resetting the score, reinitializing the positions of the shrimp and shark,
    and setting the game state to PLAYING.
    """
    global game_state, player_score, text_score_surface, shrimp_rect, shark_rect
    game_state = PLAYING
    player_score = 0
    text_score_string = f"Score: {player_score}"
    text_score_surface = font_score.render(text_score_string, True, WHITE)
    shrimp_rect.left = WIDTH
    shark_rect.centerx = WIDTH // 2
    shark_rect.centery = HEIGHT // 2


def handle_key_presses():
    """
    Handles the movement of the shark based on key presses (WASD).
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and shark_rect.top >= 0:
        shark_rect.y -= shark_speed
    elif keys[pygame.K_s] and shark_rect.bottom <= HEIGHT:
        shark_rect.y += shark_speed
    if keys[pygame.K_d] and shark_rect.right <= WIDTH:
        shark_rect.x += shark_speed
    elif keys[pygame.K_a] and shark_rect.left >= 0:
        shark_rect.x -= shark_speed


def handle_shrimp_movement():
    """
    Moves the shrimp to the left. If it moves off-screen, it reappears at a 
    random vertical position on the right.
    """
    if shrimp_rect.right >= 0:
        shrimp_rect.x -= shrimp_speed
    else:
        shrimp_rect.left = WIDTH
        shrimp_rect.centery = random.randint(20, HEIGHT - 20)


def handle_collisions():
    """
    Checks for collisions between the shark and the shrimp.
    If they collide, the score is incremented, the shrimp is repositioned, 
    and the game state is checked.
    """
    global player_score, text_score_surface, game_state
    if shark_rect.colliderect(shrimp_rect):
        shrimp_rect.left = WIDTH
        shrimp_rect.centery = random.randint(20, HEIGHT - 20)
        player_score += 1
        text_score_string = f"Score: {player_score}"
        text_score_surface = font_score.render(text_score_string, True, WHITE)
        if player_score >= 5:
            game_state = GAME_OVER


def update_animation_frames():
    """
    Updates the shark's animation frames based on the elapsed time.
    """
    global shark_frame_index, shark_time_changed
    time_now = pygame.time.get_ticks()
    if time_now - shark_time_changed > shark_frame_duration:
        shark_frame_index = (shark_frame_index + 1) % len(shark_frames)
        shark_time_changed = time_now


def draw_playing_state():
    """
    Draws the playing state, including the background, shark, shrimp, and score.
    """
    screen.blit(ocean_background, (0, 0))
    screen.blit(shark_frames[shark_frame_index], shark_rect)
    screen.blit(shrimp, shrimp_rect)
    screen.blit(text_score_surface, text_score_rect)


def draw_opening_state():
    """
    Draws the opening state, including the instructions.
    """
    screen.blit(ocean_background, (0, 0))
    screen.blit(text_instructions_surface, text_instructions_rect)
    screen.blit(text_instructions_details_surface, text_instructions_details_rect)


def draw_game_over_state():
    """
    Draws the game over state, including the game over message and final score.
    """
    screen.blit(ocean_background, (0, 0))
    screen.blit(text_game_over_surface, text_game_over_rect)
    screen.blit(text_score_surface, text_score_rect)


# Main game loop
running = True
while running:
    if not handle_events():
        break

    if game_state == PLAYING:
        handle_key_presses()
        handle_shrimp_movement()
        handle_collisions()
        update_animation_frames()
        draw_playing_state()
    elif game_state == OPENING:
        draw_opening_state()
    elif game_state == GAME_OVER:
        draw_game_over_state()
    
    pygame.display.flip()
    clock.tick(30)


# Quit Pygame   
pygame.quit()
sys.exit()

import pygame
import sys
import random
import os
import math
from spcaeinvaders_defs import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SHIP_SIZE,
    INVADER_SIZE,
    INVADER_ROWS,
    INVADERS_PER_ROW,
    INVADER_SPACING,
    PLAYER_SPEED,
    LASER_WIDTH,
    LASER_HEIGHT,
    LASER_COLOR,
    INVADER_SPEED,
    BLACK,
    WHITE,
    GREEN,
    GOLD,
    RED,
)
from spaceinvaders_effects import load_image, Laser, Explosion, VictoryEffect, GameOverEffect
from spaceinvaders_util import (
    create_invaders,
    update_lasers,
    update_explosions,
    update_game_state,
    draw_invaders,
    draw_player,
)


def move_player(current_x, move_right):
    """
    TODO: Implement this function!

    This function should move the player ship left and right across the screen.
    When the ship reaches the screen edge, it should change direction.

    Parameters:
        current_x: The current x position of the player ship
        move_right: Boolean indicating if the ship is currently moving right

    Returns:
        tuple: (new_x, new_move_right)
        - new_x: The new x position of the player ship
        - new_move_right: The new direction (True for right, False for left)

    Hints:
    1. Use PLAYER_SPEED to move the ship
    2. Check if the ship hits the screen edges (0 or SCREEN_WIDTH - SHIP_SIZE)
    3. Return both the new position and direction
    """
    # Your code goes here!
    # For now, we'll provide a basic implementation
    new_x = current_x
    new_move_right = move_right

    if move_right:
        new_x += PLAYER_SPEED
        if new_x >= SCREEN_WIDTH - SHIP_SIZE:
            new_move_right = False
    else:
        new_x -= PLAYER_SPEED
        if new_x <= 0:
            new_move_right = True

    return new_x, new_move_right


def fire_laser(player_x, player_y):
    """
    Create a new laser shot from the player's position
    Parameters:
        player_x: x-position of the player
        player_y: y-position of the player
    Returns:
        Laser: A new laser object
    """
    # Center the laser on the player ship
    laser_x = player_x + (SHIP_SIZE // 2) - (LASER_WIDTH // 2)
    return Laser(laser_x, player_y)


def InitializeGame() -> tuple[pygame.Surface, pygame.font.Font, pygame.Surface, pygame.Surface]:
    # Initialize Pygame
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders - Learning Python!")

    # Initialize font
    pygame.font.init()
    game_font = pygame.font.SysFont("Arial", 64)

    # Load game images
    player_img = load_image("player.png", (SHIP_SIZE, SHIP_SIZE))
    invader_img = load_image("invader.png", (INVADER_SIZE, INVADER_SIZE))

    return screen, game_font, player_img, invader_img


def main():
    # Set up the player
    player_x = SCREEN_WIDTH // 2 - SHIP_SIZE // 2
    player_y = SCREEN_HEIGHT - SHIP_SIZE - 10

    screen, game_font, player_img, invader_img = InitializeGame()
    # Create invaders
    invaders = create_invaders()

    # List to store active lasers and explosions
    lasers = []
    explosions = []
    victory_effect = None
    game_over_effect = None

    # Game loop
    clock = pygame.time.Clock()
    move_right = True
    shoot_delay = 0  # Counter for controlling shooting rate

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the player ship using the new function
        player_x, move_right = move_player(player_x, move_right)

        # Only shoot if game is not over
        if not victory_effect and not game_over_effect:
            shoot_delay += 1
            if shoot_delay >= 30:  # Shoot every 30 frames (about 0.5 seconds)
                lasers.append(fire_laser(player_x, player_y))
                shoot_delay = 0

        # Update lasers and check collisions
        lasers = update_lasers(lasers, invaders, explosions)

        # Update explosions
        explosions = update_explosions(explosions)

        # Check for victory/game over and update effects
        victory_effect, game_over_effect = update_game_state(invaders, victory_effect, game_over_effect)

        # Clear the screen
        screen.fill(BLACK)

        # Draw game objects
        draw_invaders(screen, invader_img, invaders)
        draw_player(screen, player_img, player_x, player_y)

        # Draw active lasers
        for laser in lasers:
            laser.draw(screen)

        # Draw active explosions
        for explosion in explosions:
            explosion.draw(screen)

        # Draw victory/game over effect if active
        if victory_effect:
            victory_effect.draw(screen, game_font)
        if game_over_effect:
            game_over_effect.draw(screen, game_font)

        # Update the display
        pygame.display.flip()

        # Control game speed
        clock.tick(60)


if __name__ == "__main__":
    main()

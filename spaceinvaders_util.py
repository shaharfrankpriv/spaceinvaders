import pygame
import sys
from spcaeinvaders_defs import *
from spaceinvaders_effects import *


def update_lasers(lasers, invaders, explosions):
    """
    Update all active lasers and check for collisions
    Parameters:
        lasers: List of active laser objects
        invaders: List of invader positions
        explosions: List of active explosions
    Returns:
        list: Updated list of invaders (with hit invaders removed)
    """
    # Move all active lasers
    for laser in lasers:
        if laser.active:
            laser.move()
            # Check for collisions with invaders
            for invader in invaders[:]:  # Create a copy to iterate over
                if laser.check_collision(invader[0], invader[1]):
                    laser.active = False  # Deactivate the laser
                    # Create explosion at invader position
                    explosions.append(Explosion(invader[0], invader[1]))
                    invaders.remove(invader)  # Remove the hit invader
                    break

    # Remove inactive lasers
    return [laser for laser in lasers if laser.active]


def update_explosions(explosions):
    """
    Update and remove finished explosions
    Parameters:
        explosions: List of active explosions
    Returns:
        list: Updated list of active explosions
    """
    for explosion in explosions:
        explosion.update()
    return [exp for exp in explosions if exp.is_active]


def draw_invaders(screen, invader_img, invaders):
    """
    Function to draw the invader ships at the top of the screen
    Parameters:
        invaders: list of invader positions (x, y)
    """
    for invader in invaders:
        screen.blit(invader_img, (invader[0], invader[1]))


def create_invaders():
    """
    Function to create the initial positions of invaders
    Returns:
        List of invader positions (x, y)
    """
    invaders = []
    for row in range(INVADER_ROWS):
        for col in range(INVADERS_PER_ROW):
            x = (col + 1) * INVADER_SPACING  # Start 100 pixels from the left
            y = row * INVADER_SPACING + 50  # Start 50 pixels from the top
            invaders.append([x, y])
    return invaders


def draw_player(screen, player_img, x, y):
    """
    Function to draw the player's ship
    Parameters:
        x: x-position of the player
        y: y-position of the player
    """
    screen.blit(player_img, (x, y))


def move_invaders(invaders):
    """
    Move all invaders down the screen
    Parameters:
        invaders: List of invader positions [x, y]
    Returns:
        bool: True if any invader has reached the bottom
    """
    reached_bottom = False
    for invader in invaders:
        invader[1] += INVADER_SPEED
        if invader[1] + INVADER_SIZE >= SCREEN_HEIGHT - SHIP_SIZE - 10:
            reached_bottom = True
    return reached_bottom


def update_game_state(invaders, victory_effect, game_over_effect):
    """
    Check for win/lose conditions and update effects
    Parameters:
        invaders: List of invader positions
        victory_effect: Current victory effect or None
        game_over_effect: Current game over effect or None
    Returns:
        tuple: (VictoryEffect or None, GameOverEffect or None)
    """
    # Check for victory
    if not invaders and victory_effect is None:
        return VictoryEffect(), None

    # Move invaders and check for game over
    if invaders and game_over_effect is None:
        if move_invaders(invaders):
            return None, GameOverEffect()

    # Update existing effects
    if victory_effect:
        victory_effect.update()
        if not victory_effect.is_active:
            pygame.quit()
            sys.exit()

    if game_over_effect:
        game_over_effect.update()
        if not game_over_effect.is_active:
            pygame.quit()
            sys.exit()

    return victory_effect, game_over_effect

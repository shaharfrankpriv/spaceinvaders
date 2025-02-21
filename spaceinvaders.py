import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHIP_SIZE = 40
INVADER_SIZE = 30
INVADER_ROWS = 3
INVADERS_PER_ROW = 8
INVADER_SPACING = 60
PLAYER_SPEED = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Learning Python!")


# Load images
def load_image(name, size):
    """
    Load an image and scale it to the desired size
    Parameters:
        name: image filename
        size: tuple of (width, height)
    Returns:
        Scaled surface
    """
    try:
        image = pygame.image.load(os.path.join("assets", name))
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Couldn't load image: {name}")
        print(e)
        # Create a colored rectangle as fallback
        surface = pygame.Surface(size)
        surface.fill(GREEN if "invader" in name else WHITE)
        return surface


# Load game images
player_img = load_image("player.png", (SHIP_SIZE, SHIP_SIZE))
invader_img = load_image("invader.png", (INVADER_SIZE, INVADER_SIZE))


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


def draw_invaders(invaders):
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
            x = col * INVADER_SPACING + 100  # Start 100 pixels from the left
            y = row * INVADER_SPACING + 50  # Start 50 pixels from the top
            invaders.append([x, y])
    return invaders


def draw_player(x, y):
    """
    Function to draw the player's ship
    Parameters:
        x: x-position of the player
        y: y-position of the player
    """
    screen.blit(player_img, (x, y))


def main():
    # Set up the player
    player_x = SCREEN_WIDTH // 2 - SHIP_SIZE // 2
    player_y = SCREEN_HEIGHT - SHIP_SIZE - 10

    # Create invaders
    invaders = create_invaders()

    # Game loop
    clock = pygame.time.Clock()
    move_right = True

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the player ship using the new function
        player_x, move_right = move_player(player_x, move_right)

        # Clear the screen
        screen.fill(BLACK)

        # Draw invaders
        draw_invaders(invaders)

        # Draw player
        draw_player(player_x, player_y)

        # Update the display
        pygame.display.flip()

        # Control game speed
        clock.tick(60)


if __name__ == "__main__":
    main()

import pygame
import sys
import random
import os
import math

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
LASER_SPEED = 7
LASER_WIDTH = 4
LASER_HEIGHT = 15
LASER_COLOR = (255, 0, 0)  # Red laser
INVADER_SPEED = 0.5  # Pixels per frame

# Explosion settings
PARTICLE_COUNT = 15
EXPLOSION_DURATION = 30  # frames
EXPLOSION_COLORS = [(255, 200, 0), (255, 150, 0), (255, 100, 0)]  # Orange-yellow colors

# Victory settings
VICTORY_PARTICLE_COUNT = 50
VICTORY_DURATION = 180  # 3 seconds at 60 FPS
VICTORY_COLORS = [(255, 215, 0), (218, 165, 32), (255, 255, 0)]  # Gold colors

# Game Over settings
GAME_OVER_PARTICLE_COUNT = 50
GAME_OVER_DURATION = 180  # 3 seconds at 60 FPS
GAME_OVER_COLORS = [(255, 0, 0), (200, 0, 0), (150, 0, 0)]  # Red colors

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GOLD = (255, 223, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Learning Python!")

# Initialize font
pygame.font.init()
game_font = pygame.font.SysFont("Arial", 64)


class Laser:
    """
    Class representing a laser shot
    This is a good example of object-oriented programming for your son
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def move(self):
        """Move the laser up the screen"""
        self.y -= LASER_SPEED
        # Deactivate if it goes off screen
        if self.y < 0:
            self.active = False

    def draw(self):
        """Draw the laser on the screen"""
        if self.active:
            pygame.draw.rect(screen, LASER_COLOR, (self.x, self.y, LASER_WIDTH, LASER_HEIGHT))

    def check_collision(self, invader_x, invader_y):
        """
        Check if the laser has hit an invader
        Returns True if there's a collision, False otherwise
        """
        if not self.active:
            return False

        # Simple rectangle collision detection
        laser_rect = pygame.Rect(self.x, self.y, LASER_WIDTH, LASER_HEIGHT)
        invader_rect = pygame.Rect(invader_x, invader_y, INVADER_SIZE, INVADER_SIZE)
        return laser_rect.colliderect(invader_rect)


class Particle:
    """
    A single particle in the explosion effect
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Random speed and direction
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.size = random.randint(2, 4)
        self.color = random.choice(EXPLOSION_COLORS)

    def move(self):
        """Move the particle"""
        self.x += self.dx
        self.y += self.dy
        self.size = max(0, self.size - 0.1)  # Gradually shrink

    def draw(self):
        """Draw the particle"""
        if self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


class Explosion:
    """
    Class representing an explosion effect
    This demonstrates particle systems and animation
    """

    def __init__(self, x, y):
        self.particles = [Particle(x + INVADER_SIZE // 2, y + INVADER_SIZE // 2) for _ in range(PARTICLE_COUNT)]
        self.duration = EXPLOSION_DURATION

    def update(self):
        """Update explosion state"""
        self.duration -= 1
        for particle in self.particles:
            particle.move()

    def draw(self):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw()

    @property
    def is_active(self):
        """Check if explosion is still active"""
        return self.duration > 0


class VictoryParticle(Particle):
    """
    Special particle for victory celebration
    Inherits from the regular Particle class
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = random.choice(VICTORY_COLORS)
        self.size = random.randint(3, 6)  # Bigger particles
        speed = random.uniform(1, 3)  # Slower movement
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed - 2  # Add upward drift
        self.fade_rate = 0.03  # Slower fade

    def move(self):
        """Move the victory particle"""
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # Add gravity effect
        self.size = max(0, self.size - self.fade_rate)


class VictoryEffect:
    """
    Special effect for victory celebration
    """

    def __init__(self):
        self.particles = []
        self.duration = VICTORY_DURATION
        self.create_particles()

    def create_particles(self):
        """Create victory particles across the screen"""
        for _ in range(VICTORY_PARTICLE_COUNT):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
            self.particles.append(VictoryParticle(x, y))

    def update(self):
        """Update victory effect"""
        self.duration -= 1
        # Add new particles periodically
        if self.duration % 10 == 0:
            self.create_particles()
        # Update existing particles
        for particle in self.particles:
            particle.move()
        # Remove faded particles
        self.particles = [p for p in self.particles if p.size > 0]

    def draw(self):
        """Draw victory effect"""
        for particle in self.particles:
            particle.draw()
        # Draw victory text
        text = game_font.render("VICTORY!", True, GOLD)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

    @property
    def is_active(self):
        """Check if victory effect is still active"""
        return self.duration > 0


class GameOverParticle(Particle):
    """
    Special particle for game over effect
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = random.choice(GAME_OVER_COLORS)
        self.size = random.randint(3, 6)
        speed = random.uniform(1, 3)
        angle = random.uniform(0.75 * math.pi, 1.25 * math.pi)  # Mostly downward
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.fade_rate = 0.03

    def move(self):
        """Move the game over particle"""
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # Add gravity effect
        self.size = max(0, self.size - self.fade_rate)


class GameOverEffect:
    """
    Special effect for game over
    """

    def __init__(self):
        self.particles = []
        self.duration = GAME_OVER_DURATION
        self.create_particles()

    def create_particles(self):
        """Create game over particles across the screen"""
        for _ in range(GAME_OVER_PARTICLE_COUNT):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            self.particles.append(GameOverParticle(x, y))

    def update(self):
        """Update game over effect"""
        self.duration -= 1
        if self.duration % 10 == 0:
            self.create_particles()
        for particle in self.particles:
            particle.move()
        self.particles = [p for p in self.particles if p.size > 0]

    def draw(self):
        """Draw game over effect"""
        for particle in self.particles:
            particle.draw()
        text = game_font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

    @property
    def is_active(self):
        """Check if game over effect is still active"""
        return self.duration > 0


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


def main():
    # Set up the player
    player_x = SCREEN_WIDTH // 2 - SHIP_SIZE // 2
    player_y = SCREEN_HEIGHT - SHIP_SIZE - 10

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
        draw_invaders(invaders)
        draw_player(player_x, player_y)

        # Draw active lasers
        for laser in lasers:
            laser.draw()

        # Draw active explosions
        for explosion in explosions:
            explosion.draw()

        # Draw victory/game over effect if active
        if victory_effect:
            victory_effect.draw()
        if game_over_effect:
            game_over_effect.draw()

        # Update the display
        pygame.display.flip()

        # Control game speed
        clock.tick(60)


if __name__ == "__main__":
    main()

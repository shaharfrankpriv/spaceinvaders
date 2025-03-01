import pygame
import random
import math
import os
from spcaeinvaders_defs import *

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

    def draw(self, screen):
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

    def draw(self, screen):
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

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)

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

    def draw(self, screen, game_font):
        """Draw victory effect"""
        for particle in self.particles:
            particle.draw(screen)
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

    def draw(self, screen, game_font):
        """Draw game over effect"""
        for particle in self.particles:
            particle.draw(screen)
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

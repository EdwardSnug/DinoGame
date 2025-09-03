import pygame
import random
import os

# Define the base directory for assets relative to this file
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(filename, fallback_size=(50, 50), color=(150, 150, 150)):
    '''
    Load image from the ASSET_DIR or create a placeholder surface if not found.
    Args:
        filename (str): The name of the image file (e.g., "Cactus.webp").
        fallback_size (tuple): (width, height) for the placeholder surface.
        color (tuple): RGB color for the placeholder surface.
    Returns:
        pygame.Surface: The loaded image or a fallback surface.
    '''
    path = os.path.join(ASSET_DIR, filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except pygame.error:
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(color)
        return surf
    except Exception:
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

class Obstacle:
    '''
    Represents an obstacle (cactus or bird) in the game.
    Handles loading images, positioning, movement, and animation.
    '''
    def __init__(self, x, ground_y):
        self.ground_y = ground_y
        self.speed = 8  # obstacle movement speed
        self.scored = False
        self.frame_counter = 0
        self.animation_index = 0
        self.image = None
        self.frames = []

        # Randomly choose obstacle type
        self.type = random.choice(["cactus_small", "cactus_tall", "bird"])

        if self.type == "cactus_small":
            self.image = load_image("Big_cacti.webp", fallback_size=(30, 70), color=(34, 139, 34))
            self.frames = [self.image]
            self.rect = self.image.get_rect(bottomleft=(x, self.ground_y + 10))

        elif self.type == "cactus_tall":
            self.image = load_image("3_Cactus_Chrome_Dino.webp", fallback_size=(45, 90), color=(34, 139, 34))
            self.frames = [self.image]
            self.rect = self.image.get_rect(bottomleft=(x, self.ground_y + 10))

        else:  # bird
            bird1 = load_image("Chrome_Pterodactyl_2.png", fallback_size=(46, 30), color=(0, 0, 0))
            bird2 = load_image("Chrome_Pterodactyl_2.png", fallback_size=(46, 30), color=(0, 0, 0))  
            self.frames = [bird1, bird2]
            self.image = self.frames[0]
            bird_height_above_ground = 83
            collision_rect_width = self.image.get_width()
            collision_rect_height = 20

            collision_rect = pygame.Rect(
                x,
                self.ground_y - bird_height_above_ground - collision_rect_height,
                collision_rect_width,
                collision_rect_height
            )
            self.rect = collision_rect

            self.draw_rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # Fallback rect if image failed
        if not self.image:
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            self.image.fill((150, 0, 0, 150))
            self.rect = self.image.get_rect(bottomleft=(x, self.ground_y))

    def update(self, speed):
        '''
        Move obstacle left and update bird animation.
        Returns:
            bool: True if obstacle is still on screen, False otherwise.
        '''
        self.rect.x -= self.speed

        if self.type == "bird":
            # Keep draw rect synced with movement
            self.draw_rect = self.image.get_rect(midbottom=(self.rect.centerx, self.rect.bottom))

            # Animate wings
            self.frame_counter += 1
            if self.frame_counter >= 6: 
                self.frame_counter = 0
                self.animation_index = (self.animation_index + 1) % len(self.frames)
                self.image = self.frames[self.animation_index]

        return self.rect.right > 0

    def draw(self, screen):
        '''
        Draw the obstacle on the screen.
        Args:
            screen (pygame.Surface): The display surface to draw on.
        '''
        if self.image:
            if self.type == "bird":
                screen.blit(self.image, self.draw_rect)
            else:
                screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

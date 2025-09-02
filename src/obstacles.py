# import pygame
# import random
# import os

# # Define the base directory for assets relative to this file
# ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

# def load_image(filename, fallback_size=(50, 50), color=(150, 150, 150)):
#     '''
#     Load image from the ASSET_DIR or create a placeholder surface if not found.
#     Args:
#         filename (str): The name of the image file (e.g., "Cactus.webp").
#         fallback_size (tuple): (width, height) for the placeholder surface.
#         color (tuple): RGB color for the placeholder surface.
#     Returns:
#         pygame.Surface: The loaded image or a fallback surface.
#     '''
#     path = os.path.join(ASSET_DIR, filename)
#     try:
#         image = pygame.image.load(path).convert_alpha()
#         #print(f"[DEBUG] Loaded obstacle image: {filename}")
#         return image
#     except pygame.error as e: # Catch specific Pygame error for image loading
#         #print(f"[WARN] Failed to load obstacle image {filename}: {e}. Using fallback.")
#         surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
#         surf.fill(color) # Fill with specified color
#         return surf
#     except Exception as e: # Catch any other unexpected errors
#         #print(f"[ERROR] An unexpected error occurred loading obstacle {filename}: {e}. Using fallback.")
#         surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
#         surf.fill(color)
#         return surf

# class Obstacle:
#     '''
#     Represents an obstacle (cactus or bird) in the game.
#     Handles loading images, positioning, movement, and animation.
#     '''
#     def __init__(self, x, ground_y):
#         self.ground_y = ground_y
#         self.speed = 8 # Increased speed for more challenge
#         self.scored = False
#         self.frame_counter = 0
#         self.animation_index = 0
#         self.image = None # Initialize image to None
#         self.frames = [] # List to hold animation frames

#         # Randomly choose obstacle type
#         # Using specific asset names now
#         self.type = random.choice(["cactus_small", "cactus_tall", "bird"])

#         # Load images and set initial position based on type
#         if self.type == "cactus_small":
#             self.image = load_image("Big_cacti.webp", fallback_size=(30, 70), color=(34, 139, 34))
#             self.frames = [self.image] # Cacti don't animate, but keep frames list consistent
#             # Position cactus on the ground
#             self.rect = self.image.get_rect(bottomleft=(x, self.ground_y + 10))
#         elif self.type == "cactus_tall":
#             self.image = load_image("3_Cactus_Chrome_Dino.webp", fallback_size=(45, 90), color=(34, 139, 34))
#             self.frames = [self.image] # Cacti don't animate
#             # Position cactus on the ground
#             self.rect = self.image.get_rect(bottomleft=(x, self.ground_y + 10))
#         else:  # self.type == "bird"
#             # Load both bird animation frames
#             bird1 = load_image("Chrome_Pterodactyl_2.png", fallback_size=(46, 30), color=(0,0,0))
#             bird2 = load_image("Chrome_Pterodactyl_2.png", fallback_size=(46, 30), color=(0,0,0)) # Assuming you have a second frame
#             self.frames = [bird1, bird2]
            
#             # Use the first frame as the initial image
#             if self.frames:
#                 self.image = self.frames[0]
#             else: # Fallback if bird frames failed to load
#                 self.image = load_image("placeholder_bird.png", fallback_size=(46, 40), color=(0,0,0)) # Placeholder name
#                 self.frames = [self.image] # Ensure frames is not empty
            
#             collision_rect_width = self.image.get_width()
#             collision_rect_height = 20

#             #desired_bird_bottom_y = self.ground_y - 80
#             # rect_y = desired_bird_bottom_y - collision_rect_height
#             safe_collision_y = self.ground_y - 104
#             self.rect = pygame.Rect(x, safe_collision_y, collision_rect_width, collision_rect_height)

#             #self.rect = pygame.Rect(x, rect_y, collision_rect_width, collision_rect_height)

#             # This line creates a draw_rect but you also need to update its position
#             self.draw_rect = self.image.get_rect(midbottom=(self.rect.centerx, self.rect.bottom))
        
#         # Fallback rect if image loading totally failed for some reason, ensures self.rect always exists
#         if not self.image:
#              self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
#              self.image.fill((150, 0, 0, 150)) # Semi-transparent red fallback
#              self.rect = self.image.get_rect(bottomleft=(x, self.ground_y))
#              #print("[ERROR] Obstacle image and rect fallback used!")


#     def update(self, speed):
#         '''
#         Move obstacle left and update bird animation.
#         Returns:
#             bool: True if obstacle is still on screen, False otherwise.
#         '''
#         self.rect.x -= self.speed

#         # --- FIX: Update the draw_rect's position to match the collision rect's position ---
#         # This ensures the visual image moves along with the hitbox.
#         if self.type == "bird":
#             self.draw_rect.midbottom = (self.rect.centerx, self.rect.bottom)
        
#         # Animate the bird
#         if self.type == "bird" and self.frames:
#             self.frame_counter += 1
#             # Adjust animation speed (e.g., change frame every 6 update calls)
#             if self.frame_counter >= 6: 
#                 self.frame_counter = 0
#                 self.animation_index = (self.animation_index + 1) % len(self.frames)
#                 self.image = self.frames[self.animation_index]
        
#         return self.rect.right > 0 # Keep if on screen (return True), or remove (return False)


#     def draw(self, screen):
#         '''
#         Draw the obstacle on the screen.
#         Args:
#             screen (pygame.Surface): The display surface to draw on.
#         '''
#         if self.image:
#             if self.type == "bird":
#                 screen.blit(self.image, self.draw_rect)
#             else:
#                 screen.blit(self.image, self.rect)
#         else:
#             # Draw a fallback rectangle if image somehow is still None
#             pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) # Red outline

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
            # Fixed bird flying height (safe for ducking)
            # bird_y = self.ground_y - 84
            # self.rect = self.image.get_rect(midbottom=(x, bird_y))
            # self.draw_rect = self.rect.copy()
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

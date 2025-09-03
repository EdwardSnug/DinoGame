import pygame
import os

# Define the base directory for assets relative to this file
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(filename, fallback_size=(50, 50), color=(0,0,0)):
    path = os.path.join(ASSET_DIR, filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"[WARN] Failed to load image {filename}: {e}. Using fallback.")
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(color)
        return surf
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred loading {filename}: {e}. Using fallback.")
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

class Dinosaur:
    def __init__(self, x, ground_y):
        self.ground_y = ground_y
        self.x = x
        self.y = ground_y
        
        self.run_frames = []
        self.duck_frames = []
        self.image = None
        
        # Load run frames
        self._load_frame("Chrome_T-Rex_Left_Run.webp", self.run_frames)
        self._load_frame("Chrome_T-Rex_Right_Run.webp", self.run_frames)

        # Load duck frames
        self._load_frame("Chrome_T-Rex_Left_Duck.png", self.duck_frames)
        self._load_frame("Chrome_T-Rex_Right_Duck.png", self.duck_frames)

        # Set a reference rect for the running state
        if self.run_frames:
            self.image = self.run_frames[0]
        else:
            fallback_size = (88, 85)
            self.image = pygame.Surface(fallback_size, pygame.SRCALPHA)
            self.image.fill((100, 100, 100))
        
        # We'll set the rect later in the update method to handle ducking
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        
        # Store initial sizes to calculate ducking offset
        self.run_rect_height = self.run_frames[0].get_height()
        self.duck_rect_height = self.duck_frames[0].get_height()

        self.is_jumping = False
        self.is_ducking = False
        self.jump_speed = 20
        self.gravity = 1.1
        self.vel_y = 0

        self.animation_index = 0
        self.animation_counter = 0

        print(f"[DEBUG] Dinosaur initialised at {self.rect}, ground_y: {self.ground_y}")

    def _load_frame(self, filename, frame_list):
        path = os.path.join(ASSET_DIR, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            frame_list.append(image)
        except pygame.error as e:
            print(f"[ERROR] Failed to load frame {filename}: {e}. Using a placeholder for this frame.")
            fallback_frame = pygame.Surface((88, 85), pygame.SRCALPHA)
            fallback_frame.fill((200, 0, 0, 150))
            frame_list.append(fallback_frame)
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred loading frame {filename}: {e}. Using a placeholder.")
            fallback_frame = pygame.Surface((88, 85), pygame.SRCALPHA)
            fallback_frame.fill((200, 0, 0, 150))
            frame_list.append(fallback_frame)

    def update(self):
        # Handle jumping physics
        if self.is_jumping:
            self.y += self.vel_y
            self.vel_y += self.gravity

            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.vel_y = 0

        # Select correct animation frames
        if self.is_ducking and not self.is_jumping:
            frames_to_use = self.duck_frames
        else:
            frames_to_use = self.run_frames

        # Only update animation if not jumping
        if frames_to_use:
            if not self.is_jumping:  
                self.animation_counter += 1
                if self.animation_counter >= 5:
                    self.animation_counter = 0
                    self.animation_index = (self.animation_index + 1) % len(frames_to_use)
            
            self.image = frames_to_use[self.animation_index]
        else:
            fallback_size = (88, 85)
            self.image = pygame.Surface(fallback_size, pygame.SRCALPHA)
            self.image.fill((255, 0, 255))
        # The rect position must be carefully managed.
        # We recreate the rect to match the image, but maintain the midbottom position
        # Get the new rect from the current image
        new_rect = self.image.get_rect()
        
        # Keep the rect's bottom at the ground level
        if self.is_ducking and not self.is_jumping:
            # When ducking, the new rect is shorter, so we move it down to stay on the ground
            new_rect.bottom = self.ground_y
        else:
            # When running or jumping, use the original height and position
            new_rect.midbottom = (self.x, self.y)
        
        self.rect = new_rect

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

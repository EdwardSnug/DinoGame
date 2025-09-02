import pygame
import random
from dino import Dinosaur
from obstacles import Obstacle

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
GROUND_Y = 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("T-Rex Runner")

# Clock for FPS control
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
dino = None
obstacles = []
score = 0
game_speed = 5
game_over = False

def reset_game():
    """Resets all game variables for a new game."""
    global dino, obstacles, score, game_speed, game_over
    dino = Dinosaur(50, GROUND_Y)
    obstacles = []
    score = 0
    game_speed = 5
    game_over = False
    print("Game state has been reset.")

# Main game loop
running = True
reset_game()

while running:
    # --- Event Handling for both states ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
        else:
            # Player controls only active during gameplay
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not dino.is_jumping:
                        dino.is_jumping = True
                        dino.vel_y = -dino.jump_speed
                elif event.key == pygame.K_DOWN and not dino.is_jumping:
                    dino.is_ducking = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.is_ducking = False

    screen.fill(WHITE)
    
    if not game_over:
        # --- Active Game Logic ---
        # Spawn obstacles
        if not obstacles or (obstacles and obstacles[-1].rect.right < WIDTH - random.randint(300, 500)):
            obstacles.append(Obstacle(WIDTH, GROUND_Y))
        
        # Update and check collisions
        dino.update()
        obstacles_to_keep = []
        for obstacle in obstacles:
            obstacle.update(game_speed)
            if dino.rect.colliderect(obstacle.rect):
                game_over = True
                print(f"Game Over! Final Score: {score}")
                break
            if obstacle.rect.right > 0:
                obstacles_to_keep.append(obstacle)
            else:
                score += 1
        obstacles = obstacles_to_keep

        # Draw everything
        dino.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

    else:
        # --- Game Over Screen Logic ---
        game_over_text = game_over_font.render("GAME OVER", True, BLACK)
        text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(game_over_text, text_rect)
        
        restart_text = font.render("Press SPACE to Restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 60))
        screen.blit(restart_text, restart_rect)
    
    # Draw ground and score (these are always visible)
    pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
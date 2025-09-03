import pygame
import random
import sys
from dino import Dinosaur
from obstacles import Obstacle
from scores_db import init_db, save_score, get_high_scores, delete_score_by_name, update_player_name

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
GRAY = (150, 150, 150)

# Game variables
dino = None
obstacles = []
score = 0
game_speed = 5
game_over = False
player_name = ''
old_player_name = ''  # Variable to store the name before editing
selected_player_name = ''  # Variable to store the name of the player clicked

# Game Status
STATE_MENU = 0
STATE_GAME = 1
STATE_GAME_OVER = 2
STATE_HIGH_SCORES = 3
STATE_OPTIONS = 4
STATE_EDIT_NAME = 5
STATE_PLAYER_SELECTED = 6
current_state = STATE_MENU

def reset_game():
    """Resets all game variables for a new game."""
    global dino, obstacles, score, game_speed, game_over
    dino = Dinosaur(50, GROUND_Y)
    obstacles = []
    score = 0
    game_speed = 5
    game_over = False
    print("Game state has been reset.")

def draw_text(text, font_size, color, x, y):
    """A helper function to render and blit text to the screen."""
    text_surface = pygame.font.Font(None, font_size).render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    """The main game loop and state machine."""
    global current_state, player_name, score, game_over, obstacles, old_player_name, selected_player_name
    
    init_db()
    
    # Initialize game state variables before entering the loop
    reset_game()

    while True:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_state == STATE_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not player_name.strip():
                            player_name = "Player1"
                        current_state = STATE_GAME
                        reset_game()
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_OPTIONS
            
            elif current_state == STATE_GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        if not dino.is_jumping:
                            dino.is_jumping = True
                            dino.vel_y = -dino.jump_speed
                    elif event.key == pygame.K_DOWN and not dino.is_jumping:
                        dino.is_ducking = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        dino.is_ducking = False

            elif current_state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    save_score(player_name, score)
                    current_state = STATE_HIGH_SCORES
            
            elif current_state == STATE_HIGH_SCORES:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player_name = ""
                    current_state = STATE_MENU
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    high_scores = get_high_scores()
                    for i, (name, s) in enumerate(high_scores):
                        text_surface = pygame.font.Font(None, 36).render(f"{i + 1}. {name}: {s}", True, BLACK)
                        text_rect = text_surface.get_rect(center=(WIDTH / 2, 150 + i * 40))
                        
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            selected_player_name = name
                            current_state = STATE_PLAYER_SELECTED
                            break
            
            elif current_state == STATE_OPTIONS:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    delete_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 60, 200, 40)
                    edit_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 40)
                    
                    if delete_button_rect.collidepoint(mouse_x, mouse_y):
                        if player_name.strip():
                            delete_score_by_name(player_name)
                        current_state = STATE_MENU
                    elif edit_button_rect.collidepoint(mouse_x, mouse_y):
                        old_player_name = player_name
                        current_state = STATE_EDIT_NAME
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_state = STATE_MENU

            elif current_state == STATE_EDIT_NAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name.strip():
                            update_player_name(old_player_name, player_name)
                        else:
                            player_name = old_player_name
                        current_state = STATE_MENU
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        player_name = old_player_name
                        current_state = STATE_MENU
                    else:
                        player_name += event.unicode
            
            elif current_state == STATE_PLAYER_SELECTED:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    delete_rect = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2 + 20, 100, 40)
                    update_rect = pygame.Rect(WIDTH / 2 + 50, HEIGHT / 2 + 20, 100, 40)
                    
                    if delete_rect.collidepoint(mouse_x, mouse_y):
                        delete_score_by_name(selected_player_name)
                        current_state = STATE_HIGH_SCORES
                    elif update_rect.collidepoint(mouse_x, mouse_y):
                        old_player_name = selected_player_name
                        player_name = selected_player_name
                        current_state = STATE_EDIT_NAME
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_state = STATE_HIGH_SCORES
        
        # --- Game Logic and Drawing based on current state ---
        screen.fill(WHITE)
        
        if current_state == STATE_MENU:
            draw_text("Enter your name:", 50, BLACK, WIDTH / 2, HEIGHT / 2 - 50)
            
            input_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 40)
            pygame.draw.rect(screen, BLACK, input_rect, 2)
            
            draw_text(player_name, 36, BLACK, input_rect.centerx, input_rect.centery)
            
            draw_text("Press ENTER to play", 30, GRAY, WIDTH / 2, HEIGHT / 2 + 50)
            draw_text("Press ESC for options", 24, GRAY, WIDTH / 2, HEIGHT / 2 + 80)

        elif current_state == STATE_GAME:
            if not obstacles or (obstacles and obstacles[-1].rect.right < WIDTH - random.randint(300, 500)):
                obstacles.append(Obstacle(WIDTH, GROUND_Y))
            
            dino.update()
            
            obstacles_to_keep = []
            for obstacle in obstacles:
                obstacle.update(game_speed)
                if dino.rect.colliderect(obstacle.rect):
                    game_over = True
                    current_state = STATE_GAME_OVER
                    break
                if obstacle.rect.right > 0:
                    obstacles_to_keep.append(obstacle)
                else:
                    score += 1
            obstacles = obstacles_to_keep

            dino.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)

            pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
            draw_text(f"Score: {score}", 36, BLACK, 100, 30)
            draw_text(f"Player: {player_name}", 24, BLACK, WIDTH - 100, 30)

        elif current_state == STATE_GAME_OVER:
            draw_text("GAME OVER", 72, BLACK, WIDTH / 2, HEIGHT / 2 - 50)
            draw_text(f"Final Score: {score}", 40, BLACK, WIDTH / 2, HEIGHT / 2 + 10)
            draw_text("Press SPACE to see high scores", 30, GRAY, WIDTH / 2, HEIGHT / 2 + 50)

        elif current_state == STATE_HIGH_SCORES:
            draw_text("High Scores", 72, BLACK, WIDTH / 2, 80)
            
            high_scores = get_high_scores()
            if not high_scores:
                draw_text("No scores recorded yet.", 36, BLACK, WIDTH / 2, 150)
            else:
                for i, (name, s) in enumerate(high_scores):
                    text = f"{i + 1}. {name}: {s}"
                    text_surface = pygame.font.Font(None, 36).render(text, True, BLACK)
                    text_rect = text_surface.get_rect(center=(WIDTH / 2, 150 + i * 40))
                    screen.blit(text_surface, text_rect)
            
            draw_text("Click a name to manage it.", 24, GRAY, WIDTH / 2, HEIGHT - 80)
            draw_text("Press SPACE to play again", 30, GRAY, WIDTH / 2, HEIGHT - 50)

        elif current_state == STATE_OPTIONS:
            draw_text("Options", 72, BLACK, WIDTH / 2, HEIGHT / 2 - 140)
            
            delete_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 60, 200, 40)
            pygame.draw.rect(screen, BLACK, delete_button_rect, 2)
            draw_text("Delete My Scores", 30, BLACK, delete_button_rect.centerx, delete_button_rect.centery)
            
            edit_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 40)
            pygame.draw.rect(screen, BLACK, edit_button_rect, 2)
            draw_text("Edit My Name", 30, BLACK, edit_button_rect.centerx, edit_button_rect.centery)
            
            draw_text("Press ESC to return to menu", 24, GRAY, WIDTH / 2, HEIGHT - 50)

        elif current_state == STATE_EDIT_NAME:
            draw_text("Edit your name:", 50, BLACK, WIDTH / 2, HEIGHT / 2 - 50)
            
            input_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 40)
            pygame.draw.rect(screen, BLACK, input_rect, 2)
            
            draw_text(player_name, 36, BLACK, input_rect.centerx, input_rect.centery)
            
            draw_text("Press ENTER to save", 30, GRAY, WIDTH / 2, HEIGHT / 2 + 50)
            draw_text("Press ESC to cancel", 24, GRAY, WIDTH / 2, HEIGHT / 2 + 80)

        elif current_state == STATE_PLAYER_SELECTED:
            draw_text(f"Selected Player: {selected_player_name}", 40, BLACK, WIDTH / 2, HEIGHT / 2 - 50)
            
            delete_rect = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2 + 20, 100, 40)
            pygame.draw.rect(screen, BLACK, delete_rect, 2)
            draw_text("DELETE", 24, BLACK, delete_rect.centerx, delete_rect.centery)

            update_rect = pygame.Rect(WIDTH / 2 + 50, HEIGHT / 2 + 20, 100, 40)
            pygame.draw.rect(screen, BLACK, update_rect, 2)
            draw_text("UPDATE", 24, BLACK, update_rect.centerx, update_rect.centery)

            draw_text("Press ESC to go back", 24, GRAY, WIDTH / 2, HEIGHT - 50)
            
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
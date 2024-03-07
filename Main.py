import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up screen dimensions dynamically
info = pygame.display.Info()
SCREEN_WIDTH = int(info.current_w * 0.9)
SCREEN_HEIGHT = int(info.current_h * 0.9)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up dino parameters
dino_width = int(0.05 * SCREEN_WIDTH)
dino_height = int(0.1 * SCREEN_HEIGHT)
dino_x = int(0.1 * SCREEN_WIDTH)
dino_y = int(0.7 * SCREEN_HEIGHT)
dino_vel_y = 0
dino_jump_power = int(0.03 * SCREEN_HEIGHT)
max_jump_height = int(0.2 * SCREEN_HEIGHT)
dino_jump = False
dino_crawl = False

# Set up obstacles parameters
obstacle_width = int(0.025 * SCREEN_WIDTH)
obstacle_height = int(0.1 * SCREEN_HEIGHT)
obstacle_list = []
obstacle_speed = int(0.01 * SCREEN_WIDTH)
obstacle_frequency = 30
obstacle_timer = 0

# Set up score parameters
score = 0
best_score = 0

# Load dino image
dino_img = pygame.image.load("dino.png")
dino_img = pygame.transform.scale(dino_img, (dino_width, dino_height))

# Load cactus image
cactus_img = pygame.image.load("cactus.png")
cactus_img = pygame.transform.scale(cactus_img, (obstacle_width, obstacle_height))

# Load bird image
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (obstacle_width, obstacle_height))

# Set up pause button parameters
pause_button_width = 50
pause_button_height = 30
pause_button_x = SCREEN_WIDTH - pause_button_width - 10
pause_button_y = 10
pause_button_color = (100, 100, 100)

# Initialize pause state
paused = False

# Initialize clock
clock = pygame.time.Clock()

# Initialize font dynamically
font_size = int(0.04 * SCREEN_WIDTH)
font = pygame.font.Font(None, font_size)

# Game over function
def game_over():
    global best_score, score
    best_score = max(best_score, score)

    game_over_text = font.render("Game Over! Score: " + str(score) + " Best Score: " + str(best_score), True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - int(0.2 * SCREEN_WIDTH), SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    reset_game()

# Placeholder for reset_game function
def reset_game():
    global dino_y, dino_jump, dino_crawl, score, obstacle_list
    dino_y = int(0.7 * SCREEN_HEIGHT)
    dino_jump = False
    dino_crawl = False
    score = 0
    obstacle_list = []

# Main game loop
def main():
    global dino_y, dino_jump, dino_crawl, score, obstacle_list, paused, dino_vel_y, obstacle_timer

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if (
                    pause_button_x < event.pos[0] < pause_button_x + pause_button_width
                    and pause_button_y < event.pos[1] < pause_button_y + pause_button_height
                ):
                    paused = not paused

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not dino_jump:
            dino_jump = True
            dino_vel_y = -dino_jump_power

        if keys[pygame.K_DOWN]:
            dino_crawl = True
        else:
            dino_crawl = False

        # Update dino position
        dino_y += dino_vel_y
        dino_vel_y += 1

        # Limit jump height
        if dino_jump and dino_y < SCREEN_HEIGHT - max_jump_height:
            dino_jump = False

        # Keep dino within screen bounds
        if dino_y >= SCREEN_HEIGHT - dino_height - int(0.03 * SCREEN_HEIGHT):
            dino_y = SCREEN_HEIGHT - dino_height - int(0.03 * SCREEN_HEIGHT)
            dino_jump = False

        # Obstacle handling
        obstacle_timer += 1
        if obstacle_timer == obstacle_frequency:
            obstacle_timer = 0

            obstacle_type = random.choice(["cactus", "bird"])

            if obstacle_type == "cactus":
                obstacle_list.append([SCREEN_WIDTH, SCREEN_HEIGHT - obstacle_height - int(0.03 * SCREEN_HEIGHT), "cactus"])
            else:
                obstacle_list.append([SCREEN_WIDTH, SCREEN_HEIGHT - 1.5 * obstacle_height - int(0.05 * SCREEN_HEIGHT), "bird"])

        obstacle_list = [[x - obstacle_speed, y, obstacle_type] for x, y, obstacle_type in obstacle_list if x > 0]

        # Collision detection
        for obstacle_x, obstacle_y, obstacle_type in obstacle_list:
            if (
                obstacle_x < dino_x + dino_width
                and obstacle_x + obstacle_width > dino_x
                and obstacle_y < dino_y + dino_height
                and obstacle_y + obstacle_height > dino_y
            ):
                game_over()

        # Increase score when passing obstacles
        score += 1

        # Draw everything
        screen.fill(WHITE)
        screen.blit(dino_img, (dino_x, dino_y))

        for obstacle_x, obstacle_y, obstacle_type in obstacle_list:
            if obstacle_type == "cactus":
                screen.blit(cactus_img, (obstacle_x, obstacle_y))
            elif obstacle_type == "bird":
                screen.blit(bird_img, (obstacle_x, obstacle_y))

        # Draw pause button
        pygame.draw.rect(screen, pause_button_color, (pause_button_x, pause_button_y, pause_button_width, pause_button_height))
        pause_text = font.render("Pause", True, WHITE)
        screen.blit(pause_text, (pause_button_x + 10, pause_button_y + 5))

        # Display score
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (int(0.01 * SCREEN_WIDTH), int(0.01 * SCREEN_HEIGHT)))

        pygame.display.update()
        clock.tick(30)  # Adjust the frame rate as needed

if __name__ == "__main__":
    main()

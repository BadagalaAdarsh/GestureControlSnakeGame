import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Set up clock
clock = pygame.time.Clock()

# Set up fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 30)

# Set up snake properties
snake_block = 20
snake_speed = 10

# Function to display score
def show_score(score):
    score_text = score_font.render("Score: " + str(score), True, white)
    screen.blit(score_text, [10, 10])

# Function to display elapsed time
def show_time(seconds):
    time_text = score_font.render("Time: " + str(seconds) + "s", True, white)
    screen.blit(time_text, [width - 130, 10])

# Function to draw the snake
def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, red, [x, y, snake_block, snake_block])

# Main game loop
def game_loop():
    game_over = False

    # Initial position of the snake
    x1 = width // 2
    y1 = height // 2

    # Initial movement direction
    x1_change = 0
    y1_change = 0

    # Initial snake length and score
    snake_list = []
    length_of_snake = 1
    score = 0

    # Generate initial food position
    food_x = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    food_y = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    # Start time
    start_time = time.time()

    # Game loop
    while not game_over:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Wrap around the screen if the snake touches the edges
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        elif y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        screen.fill(white)
        pygame.draw.rect(screen, green, [food_x, food_y, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for snake self-collision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True

        # Draw the snake
        draw_snake(snake_list)

        # Display the score
        show_score(score)

        # Calculate elapsed time
        elapsed_time = int(time.time() - start_time)
        show_time(elapsed_time)

        pygame.display.update()

        # Check for food collision
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            score += 1

        # Set game speed
        clock.tick(snake_speed)

    # Quit Pygame
    pygame.quit()

# Start the game loop
game_loop()

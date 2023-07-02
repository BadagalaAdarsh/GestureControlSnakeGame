import cv2
import math
import mediapipe as mp
import pygame
import random
import time

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize OpenCV
cap = cv2.VideoCapture(1)
width, height = int(cap.get(3)), int(cap.get(4))

# Set up text parameters
font = cv2.FONT_HERSHEY_SIMPLEX
text_position = (int(width / 2) - 50, int(height / 2))
font_scale = 1
font_color = (0, 255, 0)
line_type = 2

# Initialize Pygame
pygame.init()

# Set up colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Set up the display
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Set up clock
clock = pygame.time.Clock()

# Set up fonts
score_font = pygame.font.SysFont(None, 30)

# Set up snake properties
snake_block = 20
snake_speed = 3

# Function to display score and time
def show_score(score, elapsed_time):
    score_text = score_font.render("Score: " + str(score) + "    Time: " + str(elapsed_time) + "s", True, white)
    screen.blit(score_text, [10, 10])

# Function to draw the snake
def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, red, [x, y, snake_block, snake_block])

# Main game loop
def game_loop():
    game_over = False

    # Initial position of the snake
    x1 = screen_width // 2
    y1 = screen_height // 2

    # Initial movement direction
    x1_change = 0
    y1_change = 0

    # Initial snake length and score
    snake_list = []
    length_of_snake = 1
    score = 0

    # Generate initial food position
    food_x = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
    food_y = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0

    # Start time
    start_time = time.time()

    # Initialize Mediapipe hands object
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
        # Game loop
        counter = 0
        while not game_over:
            ret, frame = cap.read()
            counter += 1
            if not ret:
                break

            if counter % 3 != 0:
                continue

            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Convert the frame to RGB for Mediapipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with Mediapipe
            results = hands.process(frame_rgb)

            # Check if hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get the landmark coordinates of the index finger
                    index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_finger_x = int(index_finger_landmark.x * width)
                    index_finger_y = int(index_finger_landmark.y * height)

                    # Get the landmark coordinates of the index finger's base
                    index_finger_base_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    index_finger_base_x = int(index_finger_base_landmark.x * width)
                    index_finger_base_y = int(index_finger_base_landmark.y * height)

                    # Calculate the angle of the index finger with respect to the x-axis
                    angle = math.degrees(math.atan2(index_finger_y - index_finger_base_y,
                                                     index_finger_x - index_finger_base_x))

                    # Determine the finger direction based on the angle
                    if -45 <= angle <= 45:
                        direction = 'Move Right'
                        x1_change = snake_block
                        y1_change = 0
                    elif 45 < angle <= 135:
                        direction = 'Move Down'
                        x1_change = 0
                        y1_change = snake_block
                    elif -135 <= angle < -45:
                        direction = 'Move Up'
                        x1_change = 0
                        y1_change = -snake_block
                    else:
                        direction = 'Move Left'
                        x1_change = -snake_block
                        y1_change = 0

                    # Display the direction on the frame
                    cv2.putText(frame, direction, text_position, font, font_scale, font_color, line_type)

            # Update snake position
            x1 += x1_change
            y1 += y1_change

            # Wrap around the screen if the snake touches the edges
            if x1 >= screen_width:
                x1 = 0
            elif x1 < 0:
                x1 = screen_width - snake_block
            elif y1 >= screen_height:
                y1 = 0
            elif y1 < 0:
                y1 = screen_height - snake_block

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
            elapsed_time = int(time.time() - start_time)
            show_score(score, elapsed_time)

            pygame.display.update()

            # Check for food collision
            if x1 == food_x and y1 == food_y:
                food_x = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
                food_y = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
                length_of_snake += 1
                score += 1

            # Set game speed
            clock.tick(snake_speed)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            # Display camera output in a separate window
            cv2.imshow('Camera', frame)

            # Exit loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Quit Pygame
    pygame.quit()
    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Start the game loop
game_loop()

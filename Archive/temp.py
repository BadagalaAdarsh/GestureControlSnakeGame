import cv2
import math
import mediapipe as mp

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

# Main loop
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
    while cap.isOpened():   
        ret, frame = cap.read()
        if not ret:
            break

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
                elif 45 < angle <= 135:
                    direction = 'Move Down'
                elif -135 <= angle < -45:
                    direction = 'Move up'
                else:
                    direction = 'Move Left'

                # Display the direction on the frame
                cv2.putText(frame, direction, text_position, font, font_scale, font_color, line_type)

        # Display the frame
        cv2.imshow('Hand Tracking', frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

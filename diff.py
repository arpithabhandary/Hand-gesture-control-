import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe hands detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Constants for the screen size and car properties
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 20
GRAVITY = 0.5
FRICTION = 0.05
THROTTLE = 0.346
BRAKE_FORCE = 0.5

# Create the window
cv2.namedWindow("Hill Climb Racing")

# Generate a random hill
hill = np.zeros((WIDTH,), dtype=np.int32)
for i in range(1, WIDTH):
    hill[i] = hill[i - 1] + np.random.randint(-10, 10)
hill = np.clip(hill, 0, HEIGHT - 100)

# Car properties
car_position = [100, hill[100] - CAR_HEIGHT]
car_velocity = 0
car_angle = 0

# Function to draw the scene
def draw_scene():
    frame = np.full((HEIGHT, WIDTH, 3), 255, dtype=np.uint8)

    # Draw the hill
    for x in range(WIDTH - 1):
        cv2.line(frame, (x, HEIGHT - hill[x]), (x + 1, HEIGHT - hill[x + 1]), (0, 255, 0), 2)

    # Draw the car
    car_rect = ((car_position[0], HEIGHT - car_position[1]), (CAR_WIDTH, CAR_HEIGHT), car_angle)
    box = cv2.boxPoints(car_rect).astype(np.int32)
    cv2.drawContours(frame, [box], 0, (0, 0, 255), -1)

    return frame

# Function to detect hand gestures for throttle and brake control
def detect_hand_gesture(landmarks):
    if landmarks:
        # Finger tip indices: Thumb (4), Index (8), Middle (12), Ring (16), Pinky (20)
        finger_tips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]]
        finger_base = [landmarks[3], landmarks[6], landmarks[10], landmarks[14], landmarks[18]]

        # Check if each fingertip is above its base to determine if fingers are open
        fingers_open = [tip.y < base.y for tip, base in zip(finger_tips, finger_base)]

        if all(fingers_open):  # All fingers are open
            return 'accelerate'
        elif not any(fingers_open):  # All fingers are closed (fist)
            return 'brake'
    return 'none'

# Open the webcam
cap = cv2.VideoCapture(0)

# Main game loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe
    results = hands.process(frame_rgb)

    # Draw the scene with the game graphics
    game_frame = draw_scene()

    # Draw hand landmarks and control the car
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the gesture type and adjust the car's velocity accordingly
            gesture = detect_hand_gesture(hand_landmarks.landmark)
            if gesture == 'accelerate':
                car_velocity += THROTTLE
            elif gesture == 'brake':
                car_velocity -= BRAKE_FORCE

    # Calculate the car's physics
    car_velocity -= GRAVITY
    car_position[1] += car_velocity

    # Check for collisions with the hill
    if car_position[1] <= hill[int(car_position[0])]:
        car_position[1] = hill[int(car_position[0])]
        car_velocity = 0

    # Merge the game frame with the webcam feed for a combined display
    combined_frame = cv2.addWeighted(game_frame, 0.7, frame, 0.3, 0)

    cv2.imshow("Hill Climb Racing", combined_frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
hands.close()
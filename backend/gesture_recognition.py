import cv2
import mediapipe as mp

# Set up MediaPipe Hands for gesture recognition
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def recognize_gesture(image):
    # Convert the image to RGB (MediaPipe needs RGB images)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_image)
    
    if result.multi_hand_landmarks:
        for landmarks in result.multi_hand_landmarks:
            # Draw landmarks on the image
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
    
    return image, result

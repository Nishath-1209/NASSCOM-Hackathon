import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Function to determine if a finger is extended
def is_finger_extended(lm_list, finger_tip, finger_dip):
    return lm_list[finger_tip][1] < lm_list[finger_dip][1]  # Tip is above DIP

# Function to classify gestures
def classify_gesture(lm_list):
    if not lm_list:
        return "No Hand Detected"

    # Thumb
    thumb_up = lm_list[4][0] < lm_list[3][0]  # Thumb extended left
    thumb_down = lm_list[4][0] > lm_list[3][0]  # Thumb extended right

    # Fingers (Tip above DIP means extended)
    index_finger = is_finger_extended(lm_list, 8, 6)
    middle_finger = is_finger_extended(lm_list, 12, 10)
    ring_finger = is_finger_extended(lm_list, 16, 14)
    pinky_finger = is_finger_extended(lm_list, 20, 18)

    # Classify based on detected finger positions
    if thumb_up and not any([index_finger, middle_finger, ring_finger, pinky_finger]):
        return "Thumbs Up"
    elif thumb_down and not any([index_finger, middle_finger, ring_finger, pinky_finger]):
        return "Thumbs Down"
    elif index_finger and middle_finger and not ring_finger and not pinky_finger:
        return "Victory"
    elif all([index_finger, middle_finger, ring_finger, pinky_finger]):
        return "Hello"
    elif index_finger and not any([middle_finger, ring_finger, pinky_finger]):
        return "Index Finger"
    elif thumb_up and index_finger and middle_finger and not ring_finger and not pinky_finger:
        return "All the Best"
    else:
        return "Unknown"

# Start video capture
cap = cv2.VideoCapture(0)

prev_gesture = None  # Keep track of previous gesture to avoid duplicate prints

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    detected_gesture = "No Hand Detected"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark positions
            landmarks = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((id, cx, cy))

            # Get the detected gesture
            detected_gesture = classify_gesture(landmarks)

    # Display the gesture on the screen
    cv2.putText(frame, detected_gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Print only when a new gesture is detected
    if detected_gesture != prev_gesture:
        print(f"Detected Gesture: {detected_gesture}")
        prev_gesture = detected_gesture  # Update previous gesture

    cv2.imshow("Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

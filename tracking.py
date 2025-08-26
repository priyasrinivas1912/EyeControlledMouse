import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Get screen size
screen_w, screen_h = pyautogui.size()
cam = cv2.VideoCapture(0)

# Control Variables
mode = "B"  # Default mode: Both eye and hand
dragging = False  # To track drag state

# Threshold values

PINCH_THRESHOLD = 0.05  # Hand pinch distance for left-click
TWO_FINGER_THRESHOLD = 0.04  # Hand two-finger distance for right-click
BLINK_THRESHOLD = 0.006  # Eye blink distance
SCROLL_THRESHOLD = 0.01  # Eye scrolling sensitivity

# Debounce control
last_click_time = 0
CLICK_DELAY = 0.8  # seconds
scroll_counter = 0
scroll_cooldown = 5


def switch_mode(key):
    """Switch between control modes."""
    global mode
    mode_mapping = {ord('e'): "E", ord('h'): "H", ord('b'): "B"}
    mode = mode_mapping.get(key, mode)


def move_cursor(x, y):
    """Move the cursor within screen bounds and handle fail-safe."""
    x = max(10, min(screen_w - 10, int(screen_w * x)))  # Clamp x to stay within screen bounds
    y = max(10, min(screen_h - 10, int(screen_h * y)))  # Clamp y to stay within screen bounds
    try:
        pyautogui.moveTo(x, y)
    except pyautogui.FailSafeException:
        print("Fail-safe triggered: Cursor moved too close to the screen edge.")

def draw_feedback(frame, landmark, color=(0, 255, 0), radius=5):
    """
    Draw a circle at the given landmark's position on the webcam frame.
    """
    # Convert normalized landmark coordinates to pixel coordinates
    x = int(landmark.x * frame.shape[1])
    y = int(landmark.y * frame.shape[0])
    # Draw the circle on the frame
    cv2.circle(frame, (x, y), radius, color, -1)        




def handle_hand_gestures(hand_landmarks, frame):
    """Process hand gestures."""
    global dragging
    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]


    # Cursor movement
    screen_x = index_finger.x
    screen_y = index_finger.y
    move_cursor(screen_x, screen_y)

        # Draw feedback
    draw_feedback(frame, index_finger, color=(0, 0, 255)) 

    # Drag-and-Drop
    pinch_distance = np.linalg.norm(
        np.array([index_finger.x, index_finger.y]) - np.array([thumb.x, thumb.y])
    )
    if pinch_distance < PINCH_THRESHOLD:
        if not dragging:  # Avoid repeated clicks during continuous gestures
            print("Left Click Detected")
            pyautogui.click()
            dragging = True  # Flag to ensure single click per pinch
    else:
        dragging = False  # Reset dragging when pinch is released


   


            # Two-finger gesture for right-click
    two_finger_distance = np.linalg.norm(
        np.array([middle_finger.x, middle_finger.y]) - np.array([thumb.x, thumb.y])
    )
    print(f"Two-Finger Distance: {two_finger_distance}")  # Debug two-finger distance

    if two_finger_distance < TWO_FINGER_THRESHOLD:
        print("Right Click Detected")
        pyautogui.rightClick()
        
def process_eye_control(face_landmarks, frame):
    global scroll_counter
    right_eye = face_landmarks[474]
    screen_x = right_eye.x
    screen_y = right_eye.y
    move_cursor(screen_x, screen_y)
    draw_feedback(frame, right_eye, color=(255, 0, 0))

    left_eye_top = face_landmarks[145]
    left_eye_bottom = face_landmarks[159]
    blink_distance = abs(left_eye_top.y - left_eye_bottom.y)

    if blink_distance < BLINK_THRESHOLD:
        print("Blink Detected - Left Click Triggered")
        pyautogui.click()

    scroll_distance = left_eye_top.y - left_eye_bottom.y
    print(f"Scroll Distance: {scroll_distance}")

    if scroll_distance > SCROLL_THRESHOLD:
        scroll_counter += 1
        if scroll_counter >= scroll_cooldown:
            print("Scrolling Up")
            pyautogui.scroll(5)
            scroll_counter = 0
    elif scroll_distance < -SCROLL_THRESHOLD:
        scroll_counter += 1
        if scroll_counter >= scroll_cooldown:
            print("Scrolling Down")
            pyautogui.scroll(-5)
            scroll_counter = 0
    else:
        scroll_counter = 0

 


def release_resources():
    """Release webcam and close OpenCV windows."""
    cam.release()
    cv2.destroyAllWindows()


try:
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process results
        hand_results = hands.process(rgb_frame)
        face_results = face_mesh.process(rgb_frame)

        if mode in ["E", "B"] and face_results.multi_face_landmarks:
            process_eye_control(face_results.multi_face_landmarks[0].landmark, frame)

        if mode in ["H", "B"] and hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                handle_hand_gestures(hand_landmarks, frame)

        # Show mode on webcam feed
        cv2.putText(frame, f"Mode: {mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Show webcam feed
        cv2.imshow('Enhanced Eye & Hand Controlled Mouse', frame)

        # Exit condition
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        switch_mode(key)

except KeyboardInterrupt:
    print("Exiting gracefully...")

finally:
    release_resources() 


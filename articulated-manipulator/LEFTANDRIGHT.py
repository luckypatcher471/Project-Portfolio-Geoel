import cv2 as cv
import mediapipe as mp
import requests
import numpy as np
import threading

ESP_IP = "http://192.168.52.187/"  # Change to your ESP8266 IP

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  
    min_detection_confidence=0.7,  
)

# Open Webcam
cam = cv.VideoCapture(0)

# Moving average filter for Z-axis (to reduce noise)
z_buffer = []
session = requests.Session()  # Persistent HTTP session for better performance

def send_servo_update(servo_id, angle):
    """Send servo update in a separate thread to prevent lag"""
    def request_thread():
        try:
            session.get(f"{ESP_IP}/slider?id={servo_id}&value={angle}", timeout=0.1)
        except requests.exceptions.RequestException:
            print(f"⚠ Failed to send data to ESP8266 (Servo {servo_id})")

    threading.Thread(target=request_thread, daemon=True).start()

while True:
    success, frame = cam.read()
    if not success:
        print("❌ Can't read frame from camera")
        break

    frame = cv.flip(frame, 1)  # Mirror effect
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    handDetected = hands.process(frameRGB)

    right_hand = None
    left_hand = None

    if handDetected.multi_hand_landmarks:
        for handLms, handedness in zip(handDetected.multi_hand_landmarks, handDetected.multi_handedness):
            label = handedness.classification[0].label  # "Left" or "Right"
            if label == "Right":
                right_hand = handLms
            else:
                left_hand = handLms

    # **🔥 Right Hand Controls (Servos 1, 2, 3)**
    if right_hand:
        mp_drawing.draw_landmarks(frame, right_hand, mp_hands.HAND_CONNECTIONS)

        # Get X, Y, Z coordinates of index finger tip (landmark 8)
        x_pos = right_hand.landmark[8].x  
        y_pos = right_hand.landmark[8].y  
        z_pos = right_hand.landmark[8].z  

        # Correct Y-axis mapping
        y_corrected = 1 - y_pos  
        x_corrected = 1 - x_pos  

        # Map X (Left-Right) to Servo 1 (40° to 150°)
        servo1_angle = int(40 + x_corrected * 110)  
        servo1_angle = max(40, min(150, servo1_angle))  

        # Map Y (Up-Down) to Servo 2 (40°-170°)
        servo2_angle = int(40 + y_corrected * 130)  
        servo2_angle = max(40, min(170, servo2_angle))  

        # **🔥 Z-axis Rotation (Smoother Rotation)**
        z_buffer.append(z_pos)
        if len(z_buffer) > 5:
            z_buffer.pop(0)
        z_avg = np.mean(z_buffer)  

        z_scaled = max(-0.15, min(0.15, z_avg))  
        servo3_angle = int(20 + (z_scaled + 0.15) * (160 - 20) / 0.3)  
        servo3_angle = max(20, min(160, servo3_angle))  

        # **Send Right Hand Servo Updates**
        send_servo_update(0, servo1_angle)  
        send_servo_update(1, servo2_angle)  
        send_servo_update(2, servo3_angle)  

    # **🔥 Left Hand Controls (Servos 4, 5 - Gripper)**
    if left_hand:
        mp_drawing.draw_landmarks(frame, left_hand, mp_hands.HAND_CONNECTIONS)

        # Get Y-axis movement for Servo 4
        left_y = left_hand.landmark[8].y  
        servo4_angle = int(40 + (1 - left_y) * 130)  
        servo4_angle = max(40, min(170, servo4_angle))  

        # **🔥 Proportional Hand Open/Close for Servo 5 (Gripper)**
        index_tip = left_hand.landmark[8]  
        thumb_tip = left_hand.landmark[4]  

        # Calculate distance between thumb and index finger
        distance = np.sqrt((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2)  

        # Normalize distance for smooth gripper control
        min_dist = 0.02   # Minimum distance (fully closed)
        max_dist = 0.10   # Maximum distance (fully open)

        # Scale distance to servo angle (65° - 120°)
        distance = max(min_dist, min(max_dist, distance))  # Clamping within range
        servo5_angle = int(65 + (1 - (distance - min_dist) / (max_dist - min_dist)) * 55)  
        servo5_angle = max(65, min(120, servo5_angle))  # Clamping servo range

        # **Send Left Hand Servo Updates**
        send_servo_update(3, servo4_angle)  
        send_servo_update(4, servo5_angle)  # ✅ Gripper moves only between 65° and 120°

    cv.imshow("Hand Landmarks", frame)

    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()

import cv2
import mediapipe as mp
import numpy as np
import subprocess

def detect_finger():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    box_size = 100
    box_positions = [(10, 50), (132, 50), (255, 50), (377, 50), (500, 50)]
    box_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 0)]
    active_box_index = None

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                center_x = frame.shape[1] // 2
                center_y = frame.shape[0] // 2

                green_color = (0, 255, 0)
                overlay = frame.copy()
                cv2.circle(overlay, (center_x, center_y - 150), 30, green_color, -1)

                alpha = 0.01 
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

                fingers = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
                           mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
                           mp_hands.HandLandmark.PINKY_TIP]

                for finger in fingers:
                    finger_landmark = hand_landmarks.landmark[finger]
                    finger_x = int(finger_landmark.x * frame.shape[1])
                    finger_y = int(finger_landmark.y * frame.shape[0])
                    distance = np.sqrt((finger_x - center_x) ** 2 + (finger_y - center_y + 150) ** 2)

                    if distance < 50:
                        cv2.circle(frame, (finger_x, finger_y), 10, (0, 0, 0), -2)

                        if finger == mp_hands.HandLandmark.THUMB_TIP:
                            active_box_index = 4
                            program_name = 'brightness_control.py'
                            print(f"Thumb detected, opening {program_name}")
                            subprocess.Popen(['python', program_name])
                            cap.release()
                            cv2.destroyAllWindows()
                            return
                        elif finger == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                            active_box_index = 3
                            program_name = 'volume_control.py'
                            print(f"Index finger detected, opening {program_name}")
                            subprocess.Popen(['python', program_name])
                            cap.release()
                            cv2.destroyAllWindows()
                            return
                        elif finger == mp_hands.HandLandmark.MIDDLE_FINGER_TIP:
                            active_box_index = 2
                            print("Middle finger detected...")
                        elif finger == mp_hands.HandLandmark.RING_FINGER_TIP:
                            active_box_index = 1
                            print("Ring finger detected...")
                        elif finger == mp_hands.HandLandmark.PINKY_TIP:
                            active_box_index = 0
                            print("Pinky finger detected...")

        for i, (x, y) in enumerate(box_positions):
            color = box_colors[i]
            cv2.rectangle(frame, (x, y), (x + box_size, y + box_size), color, thickness=2)
            if active_box_index == i:
                cv2.rectangle(frame, (x, y), (x + box_size, y + box_size), color, thickness=cv2.FILLED)

        cv2.imshow("Box Choosing Window", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


detect_finger()

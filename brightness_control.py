import cv2
import mediapipe as mp
import screen_brightness_control as sbc
import subprocess

print ("Move your finger down to increase the volume and do the opposite to increase the volume")
print("To close this and go to change modes template, move your finger to the left.")

def change_brightness():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    center_y = screen_height // 6
    r_center_y = screen_height // 4
    x_center_y = screen_height // 2
    y_center_y = screen_height // 1
    f_center_y = int(screen_height * 0.5)

    while True:
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        cv2.rectangle(image, (0, 0), (screen_width, center_y), (0, 255, 0), 1)
        cv2.rectangle(image, (0, center_y), (screen_width, r_center_y), (255, 0, 0), 1)
        cv2.rectangle(image, (0, r_center_y), (screen_width, f_center_y), (0, 0, 255), 1)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_x = int(index_finger_landmark.x * screen_width)
                index_finger_y = int(index_finger_landmark.y * screen_height)

                if index_finger_x < 100:
                    subprocess.Popen(['python', 'changing_mods_template.py'])
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                brightness = (index_finger_y / screen_height) * 100
                sbc.set_brightness(int(brightness))

        cv2.imshow('Wave your hand here', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    change_brightness()

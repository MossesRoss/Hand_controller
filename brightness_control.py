import cv2
import mediapipe as mp
import screen_brightness_control as sbc
import subprocess

print("""To navigate back to the template, place your index finger in the left corner of the screen.
Do the opposite if you don't want to get out of this.""")

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

                if index_finger_y < center_y:
                    sbc.set_brightness(100)
                    cv2.rectangle(image, (0, 0), (screen_width, center_y), (0, 255, 0), -1)
                elif index_finger_y < r_center_y:
                    sbc.set_brightness(70)
                    cv2.rectangle(image, (0, center_y), (screen_width, r_center_y), (255, 255, 0), -1)
                elif index_finger_y < x_center_y:
                    sbc.set_brightness(50)
                    cv2.rectangle(image, (0, r_center_y), (screen_width, x_center_y), (255, 0, 0), -1)
                elif index_finger_y < y_center_y:
                    sbc.set_brightness(20)
                    cv2.rectangle(image, (0, x_center_y), (screen_width, y_center_y), (255, 0, 255), -1)
                elif index_finger_y < f_center_y:
                    sbc.set_brightness(0)
                    cv2.rectangle(image, (0, y_center_y), (screen_width, f_center_y), (0, 0, 255), -1)
                else:
                    sbc.set_brightness(0)

        cv2.imshow('Wave your hand here', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

change_brightness()
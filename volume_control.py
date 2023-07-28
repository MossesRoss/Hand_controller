import cv2
import mediapipe as mp
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess

def change_volume():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Getting Volume interface
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 0x17, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()

    while True:
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

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

                # Calculate the new volume
                new_volume = 1.0 - (index_finger_y / screen_height)
                if new_volume < 0.0:
                    new_volume = 0.0
                elif new_volume > 1.0:
                    new_volume = 1.0

                # Set the volume if it's changed
                if new_volume != current_volume:
                    volume.SetMasterVolumeLevelScalar(new_volume, None)
                    current_volume = new_volume

        cv2.imshow('User Interface', image)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Move your finger down to decrease the volume and do the opposite to increase the volume.")
    print("To close this [press space bar] and go to the change_modes_template, move your index finger to the left.")
    change_volume()

import cv2
import mediapipe as mp
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess

def change_volume():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

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
            print("Issues in Camera")
            break

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_x = int(index_finger_landmark.x * screen_width)
                index_finger_y = int(index_finger_landmark.y * screen_height)

                if index_finger_x < 100:
                    subprocess.Popen(['python', 'changing_mods_template.py'])
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                # Calculate the new volume
                top_margin = 10
                bottom_margin = 10
                max_volume_y = screen_height - top_margin
                min_volume_y = bottom_margin
                new_volume = (index_finger_y - min_volume_y) / (max_volume_y - min_volume_y)
                new_volume = max(0.0, min(1.0, new_volume))

                # Set the volume if it's changed
                if new_volume != current_volume:
                    volume.SetMasterVolumeLevelScalar(1 - new_volume, None)
                    current_volume = new_volume

                # Square around the index finger & Horizontal line
                cv2.rectangle(image, (index_finger_x - 10, index_finger_y - 10), (index_finger_x + 10, index_finger_y + 10), (255, 255, 255), 2)
                cv2.line(image, (0, index_finger_y), (screen_width, index_finger_y), (0, 255, 0), 3)

        cv2.imshow('Set Volume', image)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("To close this [Press Space bar] and to go to the change modes template, move your finger to the left.")
    change_volume()

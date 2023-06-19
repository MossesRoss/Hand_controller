import cv2
import mediapipe as mp
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

VOLUME_LEVELS = [0.0, 0.3, 0.6, 1.0]
AREA_THRESHOLDS = [0.05, 0.15, 0.25]

def change_vol():
    cap = cv2.VideoCapture(0)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 0x17, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=3,
        min_detection_confidence=0.5) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))

                    thumb_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    thumb_x, thumb_y = thumb_landmark.x, thumb_landmark.y
                    index_finger_x, index_finger_y = index_finger_landmark.x, index_finger_landmark.y

                    distance = ((thumb_x - index_finger_x) ** 2 + (thumb_y - index_finger_y) ** 2) ** 0.5

                    hand_area = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x - hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x) * (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y - hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)

                    if distance < AREA_THRESHOLDS[0]:
                        new_volume = VOLUME_LEVELS[0]
                    elif distance < AREA_THRESHOLDS[1]:
                        new_volume = VOLUME_LEVELS[1]
                    elif distance < AREA_THRESHOLDS[2]:
                        new_volume = VOLUME_LEVELS[2]
                    else:
                        new_volume = VOLUME_LEVELS[3]

                    if new_volume != current_volume:
                        volume.SetMasterVolumeLevelScalar(new_volume, None)
                        current_volume = new_volume

                    volume_bar_height = int((1.0 - current_volume) * frame.shape[0])
                    cv2.rectangle(frame, (0, 0), (20, frame.shape[0]), (0, 0, 255), -1)
                    cv2.rectangle(frame, (0, volume_bar_height), (20, frame.shape[0]), (0, 255, 0), -1)

                    
                    if index_finger_x > 0.9:
                        subprocess.Popen(["python", "changing_mods_template.py"])
                        cap.release()
                        cv2.destroyAllWindows()
                        return

            cv2.imshow('Volume Control', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


change_vol()

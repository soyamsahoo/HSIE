import mediapipe as mp
import cv2
import numpy as np

class HandTracker:
    def __init__(self, max_hands=1):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.results = None

    def process_frame(self, frame):
        # Convert to RGB and process
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        # Return raw landmarks normalized [0,1]
        landmarks = []
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                landmarks.append([(lm.x, lm.y, lm.z) for lm in hand_lms.landmark])
        return landmarks

    def map_to_world(self, landmark, view_range=(10, 10, 5)):
        # Landmark is (x, y, z) in [0, 1]
        # Map to world coordinate system (Centered at 0,0,0)
        wx = (landmark[0] - 0.5) * view_range[0]
        wy = (0.5 - landmark[1]) * view_range[1]
        wz = (landmark[2]) * view_range[2] # Z is usually closer to cam if small
        return np.array([wx, wy, wz])

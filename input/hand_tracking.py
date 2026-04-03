import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def process_frame(self, frame):
        # Convert BGR image to RGB
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        landmarks = []
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                landmarks.append([(lm.x, lm.y, lm.z) for lm in hand_lms.landmark])
        return landmarks

    def get_hand_orientation(self, hand_index=0):
        # ... logic to calculate hand orientation (rotation) ...
        # Can use landmarks 0, 5, 17 to define the palm plane
        pass

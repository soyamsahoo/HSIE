import numpy as np

class GestureRecognizer:
    def __init__(self, pinch_threshold=0.05, fist_threshold=0.1):
        self.pinch_threshold = pinch_threshold
        self.fist_threshold = fist_threshold

    def is_pinch(self, landmarks):
        # Thumb tip (4) and index tip (8)
        p4 = np.array(landmarks[4])
        p8 = np.array(landmarks[8])
        return np.linalg.norm(p4 - p8) < self.pinch_threshold

    def is_fist(self, landmarks):
        # Tips of fingers (8, 12, 16, 20) closer to palm (0) than middle joints (6, 10, 14, 18)
        palm = np.array(landmarks[0])
        tips = [8, 12, 16, 20]
        mids = [6, 10, 14, 18]
        for tip, mid in zip(tips, mids):
            if np.linalg.norm(np.array(landmarks[tip]) - palm) > np.linalg.norm(np.array(landmarks[mid]) - palm):
                return False
        return True

    def is_open_palm(self, landmarks):
        # Tips further from palm than middle joints
        palm = np.array(landmarks[0])
        tips = [8, 12, 16, 20]
        mids = [6, 10, 14, 18]
        for tip, mid in zip(tips, mids):
            if np.linalg.norm(np.array(landmarks[tip]) - palm) < np.linalg.norm(np.array(landmarks[mid]) - palm):
                return False
        return True

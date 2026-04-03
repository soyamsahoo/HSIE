import numpy as np

class GestureRecognizer:
    def __init__(self, pinch_thresh=0.06, fist_thresh=0.1):
        self.pinch_thresh = pinch_thresh
        self.fist_thresh = fist_thresh

    def classify(self, landmarks):
        # 8: Index Tip, 4: Thumb Tip, 0: Wrist
        p8 = np.array(landmarks[8])
        p4 = np.array(landmarks[4])
        p0 = np.array(landmarks[0])

        # 1. Pinch Detection (Index vs Thumb)
        dist_pinch = np.linalg.norm(p8 - p4)
        if dist_pinch < self.pinch_thresh:
            return "PINCH"

        # 2. Fist Detection (Tips curled towards wrist)
        tips = [8, 12, 16, 20]
        mids = [6, 10, 14, 18]
        dist_tips = np.array([np.linalg.norm(np.array(landmarks[t]) - p0) for t in tips])
        dist_mids = np.array([np.linalg.norm(np.array(landmarks[m]) - p0) for m in mids])

        if np.all(dist_tips < dist_mids):
            return "FIST"

        return "OPEN"

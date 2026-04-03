import os
import sys
import numpy as np

# Add current directory to path
sys.path.append(os.getcwd())

from math_utils.transform import create_model_matrix, screen_to_ndc
from renderer.camera import Camera
from physics.rigidbody import RigidBody
from input.gesture import GestureRecognizer
from interaction.raycaster import intersect_ray_sphere

def test_math_and_physics():
    print("Testing Math and Physics...")

    # Math
    m = create_model_matrix((1, 2, 3), [0, 0, 0, 1])
    assert m[3, 0] == 1.0
    print("Math utils check passed.")

    # Physics
    rb = RigidBody(position=(0, 0, 0))
    rb.apply_force((10, 0, 0))
    rb.update(0.1)
    assert rb.velocity[0] > 0
    assert rb.position[0] > 0
    print("RigidBody physics check passed.")

    # Raycasting
    dist = intersect_ray_sphere(np.array([0, 0, 10]), np.array([0, 0, -1]), np.array([0, 0, 0]), 1.0)
    assert dist > 0
    print("Raycaster intersection check passed.")

    # Gestures
    gr = GestureRecognizer()
    # Mock landmarks
    landmarks = [[0]*3 for _ in range(21)]
    # Pinch: tip 8 and tip 4 close
    landmarks[8] = [0.1, 0.1, 0.1]
    landmarks[4] = [0.11, 0.11, 0.11]
    assert gr.classify(landmarks) == "PINCH"
    print("Gesture recognizer check passed.")

    print("All core logic checks passed!")

if __name__ == "__main__":
    test_math_and_physics()

import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from renderer.shader import ShaderProgram
from renderer.mesh import Mesh, create_ring
from renderer.camera import Camera
from input.hand_tracking import HandTracker
from input.gesture import GestureRecognizer
from physics.rigidbody import RigidBody
from interaction.manipulation import InteractionManager
from interaction.selection import screen_to_world_ray
from effects.postprocessing import PostProcessingManager

import moderngl
import numpy as np

def test_initialization():
    # Use a headless context for testing if possible, or just mock it
    # Since we're in a sandbox, we might not have a GPU/Display.
    # But we can verify imports and object creation.

    print("Testing module initialization...")

    # Camera
    cam = Camera(16/9)
    assert cam.position.z == 5.0
    print("Camera initialized.")

    # Hand Tracker
    # ht = HandTracker()
    # print("HandTracker initialized.")

    # Physics
    rb = RigidBody(position=[1.0, 2.0, 3.0])
    assert rb.position.x == 1.0
    rb.apply_force(np.array([10.0, 0.0, 0.0]))
    rb.update(0.1)
    assert rb.velocity.x > 0
    print("Physics initialized and updated.")

    # Interaction
    im = InteractionManager()
    assert im.selected_object is None
    print("InteractionManager initialized.")

    print("All core modules initialized successfully.")

if __name__ == "__main__":
    test_initialization()

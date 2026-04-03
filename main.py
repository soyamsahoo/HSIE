import moderngl
import moderngl_window as mglw
import numpy as np
import time
import cv2

from renderer.camera import Camera
from renderer.mesh import create_procedural_ring
from renderer.shader import ShaderProgram
from input.hand_tracking import HandTracker
from input.gesture import GestureRecognizer
from physics.rigidbody import RigidBody
from interaction.manager import InteractionManager
from effects.post_processing import PostProcessingManager
from effects.particles import ParticleSystem
from math_utils.transform import create_model_matrix

class HolographicEngine(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Iron Man Holographic Engine"
    window_size = (1280, 720)
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = self.wnd.ctx
        self.camera = Camera(self.window_size[0] / self.window_size[1])

        # Load Shaders
        with open('renderer/hologram.vert', 'r') as f: vert_src = f.read()
        with open('renderer/hologram.frag', 'r') as f: frag_src = f.read()
        self.shader = ShaderProgram(self.ctx, vert_src, frag_src)

        # Create Scene Objects
        self.objects = []
        for i in range(3):
            # Outer Ring
            rb1 = RigidBody(position=((i-1)*3.5, 0.0, 0.0))
            rb1.mesh = create_procedural_ring(self.ctx, self.shader.program, 0.9, 1.0)
            self.objects.append(rb1)
            # Inner Ring
            rb2 = RigidBody(position=((i-1)*3.5, 0.0, 0.0))
            rb2.mesh = create_procedural_ring(self.ctx, self.shader.program, 0.6, 0.7)
            self.objects.append(rb2)

        # Systems
        self.hand_tracker = HandTracker()
        self.gesture_rec = GestureRecognizer()
        self.interaction = InteractionManager()
        self.post_process = PostProcessingManager(self.ctx, self.window_size[0], self.window_size[1])
        self.particles = ParticleSystem(self.ctx)

        # Capture Device
        self.cap = cv2.VideoCapture(0)
        self.last_time = time.time()

    def render(self, curr_time, frame_time):
        # --- 1. INPUT UPDATE ---
        ret, frame = self.cap.read()
        landmarks = self.hand_tracker.process_frame(frame) if ret else []
        gesture = "OPEN"
        cursor_x, cursor_y = 0.5, 0.5

        if landmarks:
            hand = landmarks[0]
            gesture = self.gesture_rec.classify(hand)
            cursor_x, cursor_y = hand[8][0], hand[8][1]

            # Map normalized hand coordinates to world space
            hand_world = self.hand_tracker.map_to_world(hand[8])
            self.camera.apply_parallax(hand[8][0]-0.5, hand[8][1]-0.5)

        # --- 2. INTERACTION UPDATE ---
        mx, my = cursor_x * self.window_size[0], cursor_y * self.window_size[1]
        self.interaction.process_input(mx, my, self.window_size[0], self.window_size[1], self.camera, gesture, self.objects, frame_time)

        # --- 3. PHYSICS UPDATE ---
        for obj in self.objects:
            obj.update(frame_time)
        self.particles.update(frame_time)

        # --- 4. RENDERING PASS (SCENE) ---
        self.post_process.use()

        # Setup Global Uniforms
        self.shader.program['m_view'].write(self.camera.view.astype('f4').tobytes())
        self.shader.program['m_proj'].write(self.camera.projection.astype('f4').tobytes())
        self.shader.program['cam_pos'].value = tuple(self.camera.position)
        self.shader.program['time'].value = curr_time
        self.shader.program['holo_color'].value = (0.0, 0.8, 1.0)

        for obj in self.objects:
            # Create Model Matrix
            m_model = create_model_matrix(obj.position, obj.orientation)
            self.shader.program['m_model'].write(m_model.tobytes())
            obj.mesh.render()

        # Particles
        vp = self.camera.get_vp_matrix()
        self.particles.render(vp)

        # --- 5. POST-PROCESSING PASS ---
        self.post_process.render(curr_time)

    def on_close(self):
        self.cap.release()

if __name__ == "__main__":
    mglw.run_window_config(HolographicEngine)

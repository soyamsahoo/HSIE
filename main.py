import moderngl
import moderngl_window as mglw
import numpy as np
from pyrr import Matrix44
import time

from renderer.camera import Camera
from renderer.mesh import create_ring
from renderer.shader import ShaderProgram
from input.hand_tracking import HandTracker
from input.gesture import GestureRecognizer
from physics.rigidbody import RigidBody
from physics.forces import apply_explosive_force
from interaction.manipulation import InteractionManager
from interaction.selection import screen_to_world_ray
from effects.postprocessing import PostProcessingManager
from effects.particles import ParticleSystem, CameraThread

class HolographicEngine(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Iron Man Holographic Interface"
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

        # Create Holographic Objects (Complex nested rings for Iron Man look)
        self.objects = []
        for i in range(3):
            group_pos = [(i-1)*3.0, 0.0, 0.0]

            # Outer Ring
            rb1 = RigidBody(position=group_pos)
            rb1.mesh = create_ring(self.ctx, self.shader.program, 0.9, 1.0)
            rb1.angular_velocity = np.array([0.0, 1.0, 0.0])
            self.objects.append(rb1)

            # Inner Ring (Rotated)
            rb2 = RigidBody(position=group_pos)
            rb2.mesh = create_ring(self.ctx, self.shader.program, 0.6, 0.7)
            rb2.angular_velocity = np.array([1.0, 0.0, 0.0])
            self.objects.append(rb2)

        # Hand Tracking
        self.hand_tracker = HandTracker()
        self.gesture_rec = GestureRecognizer()
        self.interaction = InteractionManager()
        self.cam_thread = CameraThread()

        # Systems
        self.particles = ParticleSystem(self.ctx)
        self.post_process = PostProcessingManager(self.ctx, self.window_size[0], self.window_size[1])
        self.time = 0

    def render(self, time, frame_time):
        self.time = time
        self.ctx.clear(0, 0, 0, 1)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Process Hand Landmarks (Non-blocking)
        ret, frame = self.cam_thread.read()
        if ret:
            landmarks = self.hand_tracker.process_frame(frame)
            if landmarks:
                hand = landmarks[0]
                is_pinch = self.gesture_rec.is_pinch(hand)
                is_fist = self.gesture_rec.is_fist(hand)

                # Cursor position
                hx, hy = hand[8][0] * self.window_size[0], (1.0 - hand[8][1]) * self.window_size[1]
                ray_origin = self.camera.position
                ray_dir = screen_to_world_ray(hx, hy, self.window_size[0], self.window_size[1], self.camera.view, self.camera.projection)

                if is_pinch:
                    if not self.interaction.selected_object:
                        self.interaction.select(self.objects, ray_origin, ray_dir)
                    self.interaction.drag(ray_origin, ray_dir, frame_time)
                    self.particles.emit(self.interaction.selected_object.position if self.interaction.selected_object else ray_origin + ray_dir * 5, 2)
                elif is_fist:
                    for obj in self.objects:
                        apply_explosive_force(obj, ray_origin + ray_dir * 5, 50.0)
                else:
                    self.interaction.release()

        # Update Systems
        self.particles.update(frame_time)

        # Scene Rendering
        self.post_process.use()

        mvp = self.camera.projection * self.camera.view
        self.shader.program['m_view'].write(self.camera.view.astype('f4').tobytes())
        self.shader.program['m_proj'].write(self.camera.projection.astype('f4').tobytes())
        self.shader.program['cam_pos'].value = tuple(self.camera.position)
        self.shader.program['time'].value = self.time
        self.shader.program['holo_color'].value = (0.0, 0.8, 1.0)

        for obj in self.objects:
            obj.update(frame_time)
            # Update rotation from angular velocity
            # (Simplification: just rotate around axis for demo)
            m_model = np.eye(4, dtype='f4')
            m_model[3, :3] = obj.position

            # Add some automatic rotation
            rot_y = Matrix44.from_y_rotation(time * obj.angular_velocity[1])
            rot_x = Matrix44.from_x_rotation(time * obj.angular_velocity[0])
            m_model = (Matrix44(m_model) * rot_y * rot_x).astype('f4')

            self.shader.program['m_model'].write(m_model.tobytes())
            obj.mesh.render()

        self.particles.render(mvp)
        self.post_process.render(time)

    def on_close(self):
        self.cam_thread.stop()

if __name__ == "__main__":
    mglw.run_window_config(HolographicEngine)

import numpy as np
from pyrr import Vector3, Quaternion

class RigidBody:
    def __init__(self, position=(0.0, 0.0, 0.0), mass=1.0):
        self.position = np.array(position, dtype='f4')
        self.velocity = np.zeros(3, dtype='f4')
        self.acceleration = np.zeros(3, dtype='f4')
        self.orientation = Quaternion([0.0, 0.0, 0.0, 1.0])
        self.angular_velocity = np.zeros(3, dtype='f4')
        self.mass = mass
        self.drag = 0.95
        self.angular_drag = 0.98

    def apply_force(self, force):
        self.acceleration += np.array(force, dtype='f4') / self.mass

    def update(self, dt):
        # 1. Integrate Velocity
        self.velocity += self.acceleration * dt
        self.velocity *= self.drag

        # 2. Integrate Position
        self.position += self.velocity * dt

        # 3. Integrate Angular Velocity (Simple implementation)
        # self.orientation *= Quaternion.from_axis_rotation(self.angular_velocity, dt)
        self.angular_velocity *= self.angular_drag

        # 4. Reset Acceleration for next frame
        self.acceleration[:] = 0.0

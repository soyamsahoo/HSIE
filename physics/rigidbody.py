import numpy as np
from pyrr import Vector3, Quaternion

class RigidBody:
    def __init__(self, position=None, mass=1.0):
        self.position = Vector3(position or [0.0, 0.0, 0.0])
        self.velocity = Vector3([0.0, 0.0, 0.0])
        self.acceleration = Vector3([0.0, 0.0, 0.0])
        self.orientation = Quaternion([0.0, 0.0, 0.0, 1.0])
        self.angular_velocity = Vector3([0.0, 0.0, 0.0])
        self.mass = mass
        self.drag = 0.95 # Simple linear damping

    def apply_force(self, force):
        self.acceleration += force / self.mass

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.velocity *= self.drag
        self.acceleration = Vector3([0.0, 0.0, 0.0])

        # Simple angular update (can expand with proper inertia tensors later)
        # self.orientation *= Quaternion.from_axis_rotation(self.angular_velocity, dt)
        pass

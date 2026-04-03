import numpy as np
from pyrr import Matrix44, Vector3

class Camera:
    def __init__(self, aspect_ratio, fov=45.0, near=0.1, far=100.0):
        self.aspect_ratio = aspect_ratio
        self.fov = fov
        self.near = near
        self.far = far
        self.position = Vector3([0.0, 0.0, 5.0])
        self.target = Vector3([0.0, 0.0, 0.0])
        self.up = Vector3([0.0, 1.0, 0.0])

        self.projection = Matrix44.perspective_projection(fov, aspect_ratio, near, far)
        self.view = Matrix44.look_at(self.position, self.target, self.up)

    def update_view(self):
        self.view = Matrix44.look_at(self.position, self.target, self.up)

    def set_aspect_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio
        self.projection = Matrix44.perspective_projection(self.fov, aspect_ratio, self.near, self.far)

    def orbit(self, distance, angle_x, angle_y):
        self.position.x = distance * np.cos(angle_y) * np.sin(angle_x)
        self.position.y = distance * np.sin(angle_y)
        self.position.z = distance * np.cos(angle_y) * np.cos(angle_x)
        self.update_view()

    def set_parallax(self, offset_x, offset_y):
        # Slightly offset position based on hand/head movement
        p_offset = Vector3([offset_x, offset_y, 0.0])
        self.view = Matrix44.look_at(self.position + p_offset, self.target, self.up)

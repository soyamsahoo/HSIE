import numpy as np
from pyrr import Matrix44, Vector3

class Camera:
    def __init__(self, aspect, fov=45.0, near=0.1, far=100.0):
        self.aspect = aspect
        self.fov = fov
        self.near = near
        self.far = far
        self.position = Vector3([0.0, 0.0, 10.0])
        self.target = Vector3([0.0, 0.0, 0.0])
        self.up = Vector3([0.0, 1.0, 0.0])

        self.projection = Matrix44.perspective_projection(fov, aspect, near, far)
        self.view = Matrix44.look_at(self.position, self.target, self.up)

    def update_aspect(self, aspect):
        self.aspect = aspect
        self.projection = Matrix44.perspective_projection(self.fov, aspect, self.near, self.far)

    def set_look_at(self, position, target):
        self.position = Vector3(position)
        self.target = Vector3(target)
        self.view = Matrix44.look_at(self.position, self.target, self.up)

    def apply_parallax(self, dx, dy, intensity=0.5):
        # Slightly offset camera position based on normalized input
        p_offset = Vector3([dx * intensity, dy * intensity, 0.0])
        self.view = Matrix44.look_at(self.position + p_offset, self.target, self.up)

    def get_vp_matrix(self):
        return (self.projection * self.view).astype('f4')

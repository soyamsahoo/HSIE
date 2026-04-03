import numpy as np
from pyrr import Vector3, Matrix44

def screen_to_world_ray(mx, my, width, height, view_mat, proj_mat):
    # Normalized device coordinates (NDC)
    x = (2.0 * mx) / width - 1.0
    y = 1.0 - (2.0 * my) / height

    # Clip coordinates (Homogeneous)
    ray_clip = np.array([x, y, -1.0, 1.0], dtype='f4')

    # Eye coordinates (View space)
    inv_proj = proj_mat.inverse
    ray_eye = inv_proj * ray_clip
    ray_eye = np.array([ray_eye[0], ray_eye[1], -1.0, 0.0], dtype='f4')

    # World coordinates
    inv_view = view_mat.inverse
    ray_world = inv_view * ray_eye
    ray_world = Vector3([ray_world[0], ray_world[1], ray_world[2]])
    ray_world = ray_world.normalized

    return ray_world

def intersect_ray_sphere(origin, direction, center, radius):
    # Standard quadratic solution
    oc = origin - center
    b = np.dot(oc, direction)
    c = np.dot(oc, oc) - radius * radius
    h = b*b - c
    if h < 0.0: return -1.0 # No intersection
    return -b - np.sqrt(h) # Distance to nearest intersection

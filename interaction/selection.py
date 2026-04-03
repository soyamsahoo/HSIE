import numpy as np
from pyrr import Vector3, Matrix44

def screen_to_world_ray(mx, my, width, height, view_mat, proj_mat):
    # Normalized device coordinates (NDC)
    x = (2.0 * mx) / width - 1.0
    y = 1.0 - (2.0 * my) / height
    z = 1.0

    ray_ndc = Vector3([x, y, z])
    ray_clip = Vector3([x, y, -1.0, 1.0]) # Homogeneous clip coords

    inv_proj = proj_mat.inverse
    inv_view = view_mat.inverse

    ray_eye = inv_proj * ray_clip
    ray_eye = Vector3([ray_eye.x, ray_eye.y, -1.0, 0.0]) # Direction, not position

    ray_world = (inv_view * ray_eye).xyz
    ray_world = ray_world.normalized

    return ray_world

def intersect_ray_sphere(ray_origin, ray_direction, sphere_center, sphere_radius):
    # Standard quadratic solution
    oc = ray_origin - sphere_center
    b = np.dot(oc, ray_direction)
    c = np.dot(oc, oc) - sphere_radius * sphere_radius
    h = b*b - c
    if h < 0.0: return -1.0 # No intersection
    return -b - np.sqrt(h) # Nearest intersection distance

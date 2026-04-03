import numpy as np
from pyrr import Matrix44, Quaternion, Vector3

def create_model_matrix(position, rotation_quat, scale=(1.0, 1.0, 1.0)):
    # Translation Matrix
    translation = Matrix44.from_translation(position)
    # Rotation Matrix from Quaternion
    rotation = Matrix44.from_quaternion(rotation_quat)
    # Scale Matrix
    scale_mat = Matrix44.from_scale(scale)
    # Combine (M = T * R * S)
    return (translation * rotation * scale_mat).astype('f4')

def lerp(a, b, t):
    return a + (b - a) * t

def screen_to_ndc(mx, my, width, height):
    # Normalized Device Coordinates (-1 to 1)
    x = (2.0 * mx) / width - 1.0
    y = 1.0 - (2.0 * my) / height
    return x, y

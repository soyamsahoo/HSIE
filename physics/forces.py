import numpy as np

def calculate_spring_force(pos, target, vel, k=10.0, c=0.5):
    # F = -k*x - c*v
    displacement = pos - target
    force = -k * displacement - c * vel
    return force

def apply_explosive_impulse(rigidbody, center, strength=50.0):
    diff = rigidbody.position - center
    dist = np.linalg.norm(diff)
    if dist < 0.1: dist = 0.1
    # Impulse = force * dt (Simplified)
    force = (diff / dist) * (strength / (dist * dist))
    rigidbody.apply_force(force)

def check_collision(pos_a, rad_a, pos_b, rad_b):
    # Simple bounding sphere collision
    dist = np.linalg.norm(pos_a - pos_b)
    return dist < (rad_a + rad_b)

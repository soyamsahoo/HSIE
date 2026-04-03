from pyrr import Vector3

def calculate_spring_force(pos, target_pos, vel, k, c):
    # F = -k*x - c*v (Spring force + damping)
    displacement = pos - target_pos
    force = -k * displacement - c * vel
    return force

def apply_explosive_force(rigidbody, center, strength):
    # F = strength * normalized(r) / distance^2
    diff = rigidbody.position - center
    dist = diff.length
    if dist < 0.1: dist = 0.1 # Prevent singularity
    force = diff.normalized * (strength / (dist * dist))
    rigidbody.apply_force(force)

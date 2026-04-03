from pyrr import Vector3

class InteractionManager:
    def __init__(self, spring_k=10.0, damping_c=0.5):
        self.spring_k = spring_k
        self.damping_c = damping_c
        self.selected_object = None
        self.grab_distance = 0.0

    def select(self, objects, ray_origin, ray_direction):
        from interaction.selection import intersect_ray_sphere
        nearest_dist = float('inf')
        nearest_obj = None
        for obj in objects:
            dist = intersect_ray_sphere(ray_origin, ray_direction, obj.position, 1.0)
            if dist > 0.0 and dist < nearest_dist:
                nearest_dist = dist
                nearest_obj = obj
        self.selected_object = nearest_obj
        self.grab_distance = nearest_dist
        return self.selected_object

    def drag(self, ray_origin, ray_direction, dt):
        if self.selected_object:
            target_pos = ray_origin + ray_direction * self.grab_distance
            # Apply spring force to snap-back object
            from physics.forces import calculate_spring_force
            f = calculate_spring_force(self.selected_object.position, target_pos, self.selected_object.velocity, self.spring_k, self.damping_c)
            self.selected_object.apply_force(f)
            self.selected_object.update(dt)

    def release(self):
        self.selected_object = None

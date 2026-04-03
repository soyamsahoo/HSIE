import numpy as np
from interaction.raycaster import screen_to_world_ray, intersect_ray_sphere
from physics.forces import calculate_spring_force, apply_explosive_impulse

class InteractionManager:
    def __init__(self, spring_k=10.0, damping_c=0.5):
        self.spring_k = spring_k
        self.damping_c = damping_c
        self.selected_object = None
        self.grab_dist = 0.0

    def process_input(self, mx, my, width, height, camera, gesture, objects, dt):
        # 1. Convert Screen to World Ray
        ray_origin = camera.position
        ray_dir = screen_to_world_ray(mx, my, width, height, camera.view, camera.projection)

        # 2. Gesture logic
        if gesture == "PINCH":
            if not self.selected_object:
                # Find nearest object intersection
                nearest_dist = float('inf')
                for obj in objects:
                    dist = intersect_ray_sphere(ray_origin, ray_dir, obj.position, 1.0)
                    if 0.0 < dist < nearest_dist:
                        nearest_dist = dist
                        self.selected_object = obj
                        self.grab_dist = dist

            if self.selected_object:
                # Apply spring force to drag object
                target_pos = ray_origin + ray_dir * self.grab_dist
                f = calculate_spring_force(self.selected_object.position, target_pos, self.selected_object.velocity, self.spring_k, self.damping_c)
                self.selected_object.apply_force(f)

        elif gesture == "FIST":
            # Explosion at cursor
            center = ray_origin + ray_dir * 5.0
            for obj in objects:
                apply_explosive_impulse(obj, center, 100.0)
            self.selected_object = None

        else: # OPEN
            self.selected_object = None

        return self.selected_object

import numpy as np
import moderngl

class Mesh:
    def __init__(self, ctx, program, vertices, indices=None):
        self.ctx = ctx
        self.program = program
        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())
        if indices is not None:
            self.ibo = ctx.buffer(indices.astype('i4').tobytes())
            self.vao = ctx.vertex_array(program, [(self.vbo, '3f 3f', 'in_position', 'in_normal')], self.ibo)
        else:
            self.vao = ctx.vertex_array(program, [(self.vbo, '3f 3f', 'in_position', 'in_normal')])

    def render(self, mode=moderngl.TRIANGLES):
        self.vao.render(mode)

    def release(self):
        self.vbo.release()
        if hasattr(self, 'ibo'):
            self.ibo.release()
        self.vao.release()

def create_ring(ctx, program, inner_radius, outer_radius, segments=64):
    vertices = []
    indices = []
    for i in range(segments + 1):
        angle = 2 * np.pi * i / segments
        c, s = np.cos(angle), np.sin(angle)

        # Outer vertex
        vertices.extend([c * outer_radius, s * outer_radius, 0.0, 0.0, 0.0, 1.0])
        # Inner vertex
        vertices.extend([c * inner_radius, s * inner_radius, 0.0, 0.0, 0.0, 1.0])

        if i < segments:
            base = 2 * i
            indices.extend([base, base + 1, base + 2])
            indices.extend([base + 1, base + 3, base + 2])

    return Mesh(ctx, program, np.array(vertices), np.array(indices))

def create_cube(ctx, program):
    # Standard 1x1x1 cube with normals
    vertices = np.array([
        # Position, Normal
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
        -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
        # ... other faces ...
    ])
    # For brevity, let's just implement a simple wireframe cube or more complete later.
    # Actually, a simple procedural sphere or ring is more "holographic".
    return Mesh(ctx, program, vertices)

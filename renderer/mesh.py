import numpy as np
import moderngl

class Mesh:
    def __init__(self, ctx, program, vertices, indices=None, format='3f 3f'):
        self.ctx = ctx
        self.program = program
        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())
        if indices is not None:
            self.ibo = ctx.buffer(indices.astype('i4').tobytes())
            self.vao = ctx.vertex_array(program, [(self.vbo, format, 'in_position', 'in_normal')], self.ibo)
        else:
            self.vao = ctx.vertex_array(program, [(self.vbo, format, 'in_position', 'in_normal')])

    def render(self, mode=moderngl.TRIANGLES):
        self.vao.render(mode)

    def release(self):
        self.vbo.release()
        if hasattr(self, 'ibo'):
            self.ibo.release()
        self.vao.release()

def create_procedural_ring(ctx, program, inner, outer, segments=64):
    # Generates vertices and indices for a 3D ring mesh
    # Interleaved: Position(3f), Normal(3f)
    vertices = []
    indices = []
    for i in range(segments + 1):
        angle = 2 * np.pi * i / segments
        c, s = np.cos(angle), np.sin(angle)
        # Outer
        vertices.extend([c * outer, s * outer, 0.0, 0.0, 0.0, 1.0])
        # Inner
        vertices.extend([c * inner, s * inner, 0.0, 0.0, 0.0, 1.0])

        if i < segments:
            b = 2 * i
            indices.extend([b, b + 1, b + 2])
            indices.extend([b + 1, b + 3, b + 2])

    return Mesh(ctx, program, np.array(vertices), np.array(indices))

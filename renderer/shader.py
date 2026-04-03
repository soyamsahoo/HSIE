import moderngl

class ShaderProgram:
    def __init__(self, ctx, vert_src, frag_src):
        self.ctx = ctx
        self.program = ctx.program(
            vertex_shader=vert_src,
            fragment_shader=frag_src,
        )

    def set_uniform(self, name, value):
        if name in self.program:
            uniform = self.program[name]
            if hasattr(value, 'tobytes'):
                uniform.write(value.tobytes())
            else:
                uniform.value = value

    def release(self):
        self.program.release()

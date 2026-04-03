import moderngl

class ShaderProgram:
    def __init__(self, ctx, vertex_source, fragment_source):
        self.ctx = ctx
        self.program = ctx.program(
            vertex_shader=vertex_source,
            fragment_shader=fragment_source,
        )

    def set_uniform(self, name, value):
        if name in self.program:
            self.program[name].value = value

    def release(self):
        self.program.release()

import moderngl
import numpy as np

class ParticleSystem:
    def __init__(self, ctx, max_particles=1000):
        self.ctx = ctx
        self.max_particles = max_particles

        # CPU Buffer
        self.pos = np.zeros((max_particles, 3), dtype='f4')
        self.vel = np.zeros((max_particles, 3), dtype='f4')
        self.life = np.zeros(max_particles, dtype='f4')

        # Interleaved VBO: 3f Pos, 1f Life
        self.buffer_data = np.zeros(max_particles * 4, dtype='f4')
        self.vbo = ctx.buffer(self.buffer_data.tobytes(), dynamic=True)

        # Simple Particle Shaders
        self.program = ctx.program(
            vertex_shader='''
                #version 330
                in vec3 in_pos;
                in float in_life;
                uniform mat4 m_vp;
                out float v_life;
                void main() {
                    v_life = in_life;
                    gl_Position = m_vp * vec4(in_pos, 1.0);
                    gl_PointSize = mix(0.0, 10.0, in_life);
                }
            ''',
            fragment_shader='''
                #version 330
                in float v_life;
                out vec4 fragColor;
                void main() {
                    fragColor = vec4(0.0, 0.9, 1.0, v_life * 0.8);
                }
            '''
        )
        self.vao = ctx.vertex_array(self.program, [(self.vbo, '3f 1f', 'in_pos', 'in_life')])

    def emit(self, origin, count=5):
        # Revive dead particles
        dead = np.where(self.life <= 0)[0]
        for i in range(min(count, len(dead))):
            idx = dead[i]
            self.pos[idx] = origin
            self.vel[idx] = (np.random.rand(3) - 0.5) * 5.0
            self.life[idx] = 1.0

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt * 0.5
        self.life = np.maximum(self.life, 0)

        # Interleave pos and life for VBO
        data = np.hstack([self.pos, self.life.reshape(-1, 1)]).astype('f4')
        self.vbo.write(data.tobytes())

    def render(self, m_vp):
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE
        self.program['m_vp'].write(m_vp.astype('f4').tobytes())
        self.vao.render(moderngl.POINTS)

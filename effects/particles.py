import moderngl
import numpy as np
import threading
import cv2

class ParticleSystem:
    def __init__(self, ctx, max_particles=2000):
        self.ctx = ctx
        self.max_particles = max_particles

        # CPU storage
        self.pos = np.zeros((max_particles, 3), dtype='f4')
        self.vel = np.zeros((max_particles, 3), dtype='f4')
        self.life = np.zeros(max_particles, dtype='f4')

        # Interleaved buffer: pos(3f), life(1f)
        self.buffer_data = np.zeros(max_particles * 4, dtype='f4')
        self.vbo = ctx.buffer(self.buffer_data.tobytes(), dynamic=True)

        self.program = ctx.program(
            vertex_shader='''
                #version 330
                in vec3 in_pos;
                in float in_life;
                uniform mat4 m_view_proj;
                out float v_life;
                void main() {
                    v_life = in_life;
                    gl_Position = m_view_proj * vec4(in_pos, 1.0);
                    gl_PointSize = mix(0.0, 10.0, in_life);
                }
            ''',
            fragment_shader='''
                #version 330
                in float v_life;
                out vec4 fragColor;
                void main() {
                    vec3 cyan = vec3(0.0, 0.9, 1.0);
                    fragColor = vec4(cyan, v_life * 0.8);
                }
            '''
        )
        self.vao = ctx.vertex_array(self.program, [(self.vbo, '3f 1f', 'in_pos', 'in_life')])

    def emit(self, origin, count=5):
        # Find dead particles and revive
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

    def render(self, m_view_proj):
        self.program['m_view_proj'].write(m_view_proj.astype('f4').tobytes())
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE
        self.vao.render(moderngl.POINTS)

class CameraThread:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        self.ret, self.frame = False, None
        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.running = False
        self.cap.release()

import moderngl
import numpy as np

class PostProcessingManager:
    def __init__(self, ctx, width, height):
        self.ctx = ctx
        self.width = width
        self.height = height

        # Main Render FBO
        self.tex_color = ctx.texture((width, height), 4)
        self.fbo = ctx.framebuffer(color_attachments=[self.tex_color])

        # Bright Pass (Bloom)
        self.tex_bright = ctx.texture((width, height), 4)
        self.fbo_bright = ctx.framebuffer(color_attachments=[self.tex_bright])

        # Quad Buffer
        self.quad_buffer = ctx.buffer(np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0,  1.0, 1.0, 1.0,
        ], dtype='f4').tobytes())

        # Shaders for CRT and Bloom Combine
        self.program = ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_position;
                in vec2 in_texcoord;
                out vec2 v_texcoord;
                void main() {
                    v_texcoord = in_texcoord;
                    gl_Position = vec4(in_position, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2D tex;
                uniform float time;
                in vec2 v_texcoord;
                out vec4 fragColor;
                void main() {
                    vec4 color = texture(tex, v_texcoord);

                    // CRT Scanlines
                    float scanline = sin(v_texcoord.y * 1000.0) * 0.05;
                    color.rgb -= scanline;

                    // Vignette
                    float dist = distance(v_texcoord, vec2(0.5));
                    color.rgb *= 1.0 - smoothstep(0.4, 0.8, dist);

                    fragColor = color;
                }
            '''
        )
        self.vao = ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'in_position', 'in_texcoord')])

    def use(self):
        self.fbo.use()
        self.ctx.clear(0, 0, 0, 1)

    def render(self, time):
        self.ctx.screen.use()
        self.tex_color.use()
        self.program['time'].value = time
        self.vao.render(moderngl.TRIANGLE_STRIP)

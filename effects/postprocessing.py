import moderngl
import numpy as np

class PostProcessingManager:
    def __init__(self, ctx, width, height):
        self.ctx = ctx
        self.width = width
        self.height = height

        # 1. Main Render FBO
        self.tex_color = ctx.texture((width, height), 4)
        self.fbo = ctx.framebuffer(color_attachments=[self.tex_color])

        # 2. Bright Pass FBO (For Bloom)
        self.tex_bright = ctx.texture((width, height), 4)
        self.fbo_bright = ctx.framebuffer(color_attachments=[self.tex_bright])

        # 3. Blur FBOs (Ping-pong)
        self.tex_blur1 = ctx.texture((width // 4, height // 4), 4)
        self.fbo_blur1 = ctx.framebuffer(color_attachments=[self.tex_blur1])
        self.tex_blur2 = ctx.texture((width // 4, height // 4), 4)
        self.fbo_blur2 = ctx.framebuffer(color_attachments=[self.tex_blur2])

        # Quad Geometry
        self.quad_vbo = ctx.buffer(np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0,  1.0, 1.0, 1.0,
        ], dtype='f4').tobytes())

        # Bright Pass Shader
        self.prog_bright = ctx.program(
            vertex_shader=self.vert_src(),
            fragment_shader='''
                #version 330
                uniform sampler2D tex;
                in vec2 v_texcoord;
                out vec4 fragColor;
                void main() {
                    vec4 color = texture(tex, v_texcoord);
                    float brightness = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
                    if(brightness > 0.6) fragColor = color;
                    else fragColor = vec4(0.0, 0.0, 0.0, 1.0);
                }
            '''
        )
        self.vao_bright = ctx.vertex_array(self.prog_bright, [(self.quad_vbo, '2f 2f', 'in_position', 'in_texcoord')])

        # Blur Shader (Gaussian)
        self.prog_blur = ctx.program(
            vertex_shader=self.vert_src(),
            fragment_shader='''
                #version 330
                uniform sampler2D tex;
                uniform bool horizontal;
                in vec2 v_texcoord;
                out vec4 fragColor;
                float weight[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);
                void main() {
                    vec2 tex_offset = 1.0 / textureSize(tex, 0);
                    vec3 result = texture(tex, v_texcoord).rgb * weight[0];
                    if(horizontal) {
                        for(int i=1; i<5; ++i) {
                            result += texture(tex, v_texcoord + vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
                            result += texture(tex, v_texcoord - vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
                        }
                    } else {
                        for(int i=1; i<5; ++i) {
                            result += texture(tex, v_texcoord + vec2(0.0, tex_offset.y * i)).rgb * weight[i];
                            result += texture(tex, v_texcoord - vec2(0.0, tex_offset.y * i)).rgb * weight[i];
                        }
                    }
                    fragColor = vec4(result, 1.0);
                }
            '''
        )
        self.vao_blur = ctx.vertex_array(self.prog_blur, [(self.quad_vbo, '2f 2f', 'in_position', 'in_texcoord')])

        # Final Combine Shader
        self.prog_combine = ctx.program(
            vertex_shader=self.vert_src(),
            fragment_shader='''
                #version 330
                uniform sampler2D scene;
                uniform sampler2D bloomBlur;
                uniform float time;
                in vec2 v_texcoord;
                out vec4 fragColor;
                void main() {
                    const float exposure = 1.0;
                    const float gamma = 2.2;
                    vec3 hdrColor = texture(scene, v_texcoord).rgb;
                    vec3 bloomColor = texture(bloomBlur, v_texcoord).rgb;

                    // Add Bloom
                    hdrColor += bloomColor * 0.5;

                    // Tone mapping
                    vec3 mapped = vec3(1.0) - exp(-hdrColor * exposure);
                    mapped = pow(mapped, vec3(1.0 / gamma));

                    // CRT / Scanline effect
                    float scanline = sin(v_texcoord.y * 1000.0) * 0.05;
                    mapped -= scanline;

                    fragColor = vec4(mapped, 1.0);
                }
            '''
        )
        self.vao_combine = ctx.vertex_array(self.prog_combine, [(self.quad_vbo, '2f 2f', 'in_position', 'in_texcoord')])

    def vert_src(self):
        return '''
            #version 330
            in vec2 in_position;
            in vec2 in_texcoord;
            out vec2 v_texcoord;
            void main() {
                v_texcoord = in_texcoord;
                gl_Position = vec4(in_position, 0.0, 1.0);
            }
        '''

    def use(self):
        self.fbo.use()
        self.ctx.clear(0, 0, 0, 1)

    def render(self, time):
        # 1. Bright Pass
        self.fbo_bright.use()
        self.tex_color.use(0)
        self.vao_bright.render(moderngl.TRIANGLE_STRIP)

        # 2. Blur Pass (4 iterations)
        horizontal = True
        first_iteration = True
        for i in range(4):
            self.fbo_blur2.use() if horizontal else self.fbo_blur1.use()
            self.prog_blur['horizontal'].value = horizontal
            if first_iteration:
                self.tex_bright.use(0)
                first_iteration = False
            else:
                self.tex_blur1.use(0) if horizontal else self.tex_blur2.use(0)
            self.vao_blur.render(moderngl.TRIANGLE_STRIP)
            horizontal = not horizontal

        # 3. Combine Pass
        self.ctx.screen.use()
        self.prog_combine['time'].value = time
        self.tex_color.use(0)
        self.tex_blur1.use(1) # Final blurred texture
        self.prog_combine['scene'].value = 0
        self.prog_combine['bloomBlur'].value = 1
        self.vao_combine.render(moderngl.TRIANGLE_STRIP)

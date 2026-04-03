import moderngl
import os

def test_shader_compilation():
    print("Testing shader compilation...")
    try:
        # Create a headless context
        ctx = moderngl.create_standalone_context()

        with open('renderer/hologram.vert', 'r') as f: vert_src = f.read()
        with open('renderer/hologram.frag', 'r') as f: frag_src = f.read()

        prog = ctx.program(vertex_shader=vert_src, fragment_shader=frag_src)
        print("Hologram shader compiled successfully.")

        # Test Post-processing shaders from effects/postprocessing.py
        from effects.postprocessing import PostProcessingManager
        ppm = PostProcessingManager(ctx, 1280, 720)
        print("PostProcessingManager (and its shaders) initialized successfully.")

        # Test Particle system shaders
        from effects.particles import ParticleSystem
        ps = ParticleSystem(ctx)
        print("ParticleSystem (and its shaders) initialized successfully.")

        print("All shaders compiled successfully.")
    except Exception as e:
        print(f"Shader compilation failed: {e}")
        exit(1)

if __name__ == "__main__":
    test_shader_compilation()

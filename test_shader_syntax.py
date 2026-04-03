import os

def test_shader_syntax():
    print("Verifying shader file syntax (checking for illegal headers)...")

    files = ['renderer/hologram.vert', 'renderer/hologram.frag']
    for filepath in files:
        with open(filepath, 'r') as f:
            first_line = f.readline().strip()
            print(f"File {filepath}, First line: '{first_line}'")
            if not first_line.startswith("#version"):
                print(f"ERROR: {filepath} must start with #version")
                exit(1)

    print("Shader file syntax check passed (version directive at start).")

if __name__ == "__main__":
    test_shader_syntax()

# Holographic Fragment Shader
#version 330

in vec3 v_normal;
in vec3 v_position;

uniform vec3 cam_pos;
uniform float time;
uniform vec3 holo_color;

out vec4 fragColor;

void main() {
    // View direction
    vec3 view_dir = normalize(cam_pos - v_position);

    // Fresnel Effect (Edge Glow)
    float fresnel = 1.0 - max(dot(view_dir, v_normal), 0.0);
    fresnel = pow(fresnel, 3.0); // Edge glow falloff

    // Time-based flicker (Simulate scanning)
    float scanline = sin(v_position.y * 50.0 + time * 10.0) * 0.5 + 0.5;
    float flicker = sin(time * 20.0) * 0.05 + 0.95;

    // Simple Lighting (Specular highlights)
    float spec = pow(max(dot(reflect(-view_dir, v_normal), view_dir), 0.0), 32.0);

    // Final Color
    vec3 color = holo_color * (fresnel + 0.2 * scanline + 0.5 * spec);
    float alpha = (fresnel + 0.1 * scanline) * flicker;

    fragColor = vec4(color, alpha);
}

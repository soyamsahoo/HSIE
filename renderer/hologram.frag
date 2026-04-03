#version 330

in vec3 v_normal;
in vec3 v_position;

uniform vec3 cam_pos;
uniform float time;
uniform vec3 holo_color;

out vec4 fragColor;

void main() {
    // Normalization and Directions
    vec3 normal = normalize(v_normal);
    vec3 view_dir = normalize(cam_pos - v_position);
    vec3 light_dir = normalize(vec3(0.5, 1.0, 0.5)); // Fixed light for holo

    // 1. Fresnel Effect (Edge Glow)
    float fresnel = 1.0 - max(dot(view_dir, normal), 0.0);
    fresnel = pow(fresnel, 2.5); // Slightly softer edge

    // 2. Diffuse (Lambert) - Subtle for holograms
    float diff = max(dot(normal, light_dir), 0.0);

    // 3. Specular (Phong)
    vec3 reflect_dir = reflect(-light_dir, normal);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32.0);

    // 4. Scanning & Flicker
    float scanline = sin(v_position.y * 80.0 - time * 5.0) * 0.5 + 0.5;
    float flicker = sin(time * 30.0) * 0.02 + 0.98;

    // 5. Depth-based Fog (Fade into distance)
    float dist = length(cam_pos - v_position);
    float fog = exp(-0.05 * dist);

    // Final Composition
    vec3 base_color = holo_color;
    vec3 final_color = base_color * (0.3 + 0.7 * fresnel + 0.2 * diff + 0.8 * spec);
    final_color += base_color * scanline * 0.2; // Add scanline glow

    float alpha = (0.2 + 0.6 * fresnel + 0.1 * scanline) * fog * flicker;

    fragColor = vec4(final_color, alpha);
}

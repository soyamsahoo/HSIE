#version 330

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_proj;

out vec3 v_normal;
out vec3 v_position;

void main() {
    vec4 world_pos = m_model * vec4(in_position, 1.0);
    v_position = world_pos.xyz;
    v_normal = normalize(mat3(m_model) * in_normal);
    gl_Position = m_proj * m_view * world_pos;
}

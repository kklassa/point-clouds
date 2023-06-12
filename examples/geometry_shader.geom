#version 410 core
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 u_viewProjectionMatrix;
uniform float u_pointSize;

void main() {
    vec4 pos = u_viewProjectionMatrix * gl_in[0].gl_Position;

    gl_Position = pos + vec4(-u_pointSize, -u_pointSize, 0, 0);
    EmitVertex();
    gl_Position = pos + vec4(-u_pointSize, u_pointSize, 0, 0);
    EmitVertex();
    gl_Position = pos + vec4(u_pointSize, -u_pointSize, 0, 0);
    EmitVertex();
    gl_Position = pos + vec4(u_pointSize, u_pointSize, 0, 0);
    EmitVertex();

    EndPrimitive();
}
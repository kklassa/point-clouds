#version 410
layout (points) in;
layout (triangle_strip, max_vertices = 64) out;
uniform float size;
const float PI = 3.1415926535897932384626433832795;
const int numSegments = 32; // Number of circle segments

void main() {
    vec4 center = gl_in[0].gl_Position;

    for(int i = 0; i <= numSegments; i++) {
        float angle = 2.0 * PI * float(i) / float(numSegments);
        float cosA = cos(angle);
        float sinA = sin(angle);
        vec4 offset = vec4(cosA, sinA, 0.0, 0.0) * size;
        gl_Position = center + offset;
        EmitVertex();

        // Emit the center vertex every other vertex.
        if (i % 2 == 0) {
            gl_Position = center;
            EmitVertex();
        }
    }
    EndPrimitive();
}
#version 410
layout (location = 0) in vec3 aPos;
layout (location = 1) in float aSize;
uniform mat4 transform;
out float Size;
void main()
{
    gl_Position = transform * vec4(aPos.x, aPos.y, aPos.z, 1.0);
    Size = aSize;
}
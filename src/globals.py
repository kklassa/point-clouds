vertex_shader = """
#version 410
uniform mat4 transform;
in vec3 position;
void main()
{
    gl_Position = transform * vec4(position, 1.0);
}
"""

fragment_shader1 = """
#version 410
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
"""

fragment_shader2 = """
#version 410
out vec4 FragColor;
void main()
{
    FragColor = vec4(0.0f, 2.0f, 0.0f, 1.0f);
}
"""
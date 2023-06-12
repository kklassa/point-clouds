from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np

vertex_shader = """
#version 410
layout (location = 0) in vec3 aPos;
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

fragment_shader = """
#version 410
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
"""

geometry_shader = """
#version 410 core
layout (lines) in;
layout (line_strip, max_vertices = 2) out;

void main() {
    for (int i = 0; i < gl_in.length(); i++) {
        gl_Position = gl_in[i].gl_Position;
        EmitVertex();
    }
    EndPrimitive();
}
"""

def create_vao(points):
    points = np.array(points, dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, points.nbytes, points, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    return vao

def read_obj(filename):
    vertices = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if parts[0] == 'v':  # the line describes a vertex
                vertices.append(list(map(float, parts[1:])))

    return vertices

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(geometry_shader, GL_GEOMETRY_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    vertices = read_obj('assets\go-gopher.obj')
    vao = create_vao(vertices)

    glUseProgram(shader)

    glPointSize(4)

    while not glfw.window_should_close(window):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(vao)
        # glDrawArrays(GL_LINES_ADJACENCY, 0, len(vertices))
        glDrawArrays(GL_LINES, 0, len(vertices))

        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
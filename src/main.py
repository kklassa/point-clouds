from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np


vertex_shader = """
#version 410
uniform mat4 transform;
in vec3 position;
void main()
{
    gl_Position = transform * vec4(position, 1.0);
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

    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    vertices = read_obj('assets\go-gopher.obj') # You might have to tweak the slash as I am on Windows rn

    vao = create_vao(vertices)

    glPointSize(4)

    transform = np.array([1.0, 0.0, 0.0, 0.0,
                            0.0, 1.0, 0.0, 0.0,
                            0.0, 0.0, 1.0, 0.0,
                            0.0, -0.5, 0.0, 1.0], dtype=np.float32)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader)

        # Handle keyboard input
        translation_speed = 0.0001
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            transform[13] += translation_speed  # Move up
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            transform[13] -= translation_speed  # Move down
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            transform[12] -= translation_speed  # Move left
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            transform[12] += translation_speed  # Move right
        
        transformLoc = glGetUniformLocation(shader, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, transform)

        glBindVertexArray(vao)
        glDrawArrays(GL_POINTS, 0, len(vertices)//3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

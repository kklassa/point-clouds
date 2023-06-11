from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np

vertex_shader = """
#version 410
layout (location = 0) in vec3 aPos;
uniform float zoom;
uniform float pan_x;
uniform float pan_y;
void main()
{
    gl_Position = vec4((aPos.x + pan_x) * zoom, (aPos.y + pan_y) * zoom, aPos.z, 1.0);
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

zoom = 1.0
pan = [0.0, 0.0]
last_mouse_pos = [0, 0]
is_middle_mouse_button_pressed = False

def scroll_callback(window, x_offset, y_offset):
    global zoom
    zoom += y_offset * 0.1
    zoom = max(0.1, zoom)

def cursor_position_callback(window, xpos, ypos):
    global last_mouse_pos
    global pan
    if is_middle_mouse_button_pressed:
        dx = xpos - last_mouse_pos[0]
        dy = ypos - last_mouse_pos[1]
        pan[0] += dx * 0.001
        pan[1] -= dy * 0.001  # y is inverted
    last_mouse_pos = [xpos, ypos]

def mouse_button_callback(window, button, action, mods):
    global is_middle_mouse_button_pressed
    if button == glfw.MOUSE_BUTTON_MIDDLE:
        is_middle_mouse_button_pressed = action == glfw.PRESS

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

def main():
    global zoom
    global pan

    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    points = [
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0
    ]

    vao = create_vao(points)

    glUseProgram(shader)

    glPointSize(4)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUniform1f(glGetUniformLocation(shader, "zoom"), zoom)
        glUniform1f(glGetUniformLocation(shader, "pan_x"), pan[0])
        glUniform1f(glGetUniformLocation(shader, "pan_y"), pan[1])

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

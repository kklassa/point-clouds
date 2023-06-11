from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import glm
import numpy as np

vertex_shader = """
#version 410
layout (location = 0) in vec3 aPos;
uniform mat4 transform;
void main()
{
    gl_Position = transform * vec4(aPos.x, aPos.y, aPos.z, 1.0);
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
is_right_mouse_button_pressed = False
rotation_angle = [0.0, 0.0]  # in radians

def scroll_callback(window, x_offset, y_offset):
    global zoom
    zoom += y_offset * 0.1
    zoom = max(0.1, zoom)

def cursor_position_callback(window, xpos, ypos):
    global last_mouse_pos
    global pan
    dx = xpos - last_mouse_pos[0]
    dy = ypos - last_mouse_pos[1]
    if is_middle_mouse_button_pressed:
        pan[0] += dx * 0.0025
        pan[1] -= dy * 0.0025  # y is inverted
    elif is_right_mouse_button_pressed:
        rotation_angle[0] += dy * 0.01
        rotation_angle[1] += dx * 0.01
    last_mouse_pos = [xpos, ypos]

def mouse_button_callback(window, button, action, mods):
    global is_middle_mouse_button_pressed
    global is_right_mouse_button_pressed
    if button == glfw.MOUSE_BUTTON_MIDDLE:
        is_middle_mouse_button_pressed = action == glfw.PRESS
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        is_right_mouse_button_pressed = action == glfw.PRESS

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

        transform = glm.mat4(1)  # Identity matrix
        transform = glm.translate(transform, glm.vec3(pan[0], pan[1], 0.0))
        transform = glm.scale(transform, glm.vec3(zoom, zoom, zoom))
        transform = glm.rotate(transform, rotation_angle[0], glm.vec3(1.0, 0.0, 0.0))
        transform = glm.rotate(transform, rotation_angle[1], glm.vec3(0.0, 1.0, 0.0))

        glUniformMatrix4fv(glGetUniformLocation(shader, "transform"), 1, GL_FALSE, glm.value_ptr(transform))

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

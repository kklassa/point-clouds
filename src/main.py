from OpenGL.GL import *
import glfw
import glm
import numpy as np

from globals import vertex_shader, fragment_shader1, fragment_shader2
from object import Object


ZOOM = 1.0
PAN = [0.0, 0.0]
LAST_MOUSE_PAN = [0, 0]
IS_MIDDLE_MOUSE_BUTTON_PRESSED = False
IS_RIGHT_MOUSE_BUTTON_PRESSED = False
ROTATION_ANGLE = [0.0, 0.0]  # in radians


def scroll_callback(window, x_offset, y_offset):
    global ZOOM
    ZOOM += y_offset * 0.2
    ZOOM = max(0.1, ZOOM)


def cursor_position_callback(window, xpos, ypos):
    global LAST_MOUSE_PAN
    global PAN
    dx = xpos - LAST_MOUSE_PAN[0]
    dy = ypos - LAST_MOUSE_PAN[1]
    if IS_MIDDLE_MOUSE_BUTTON_PRESSED:
        PAN[0] += dx * 0.0025
        PAN[1] -= dy * 0.0025  # y is inverted
    elif IS_RIGHT_MOUSE_BUTTON_PRESSED:
        ROTATION_ANGLE[0] += dy * 0.01
        ROTATION_ANGLE[1] += dx * 0.01
    LAST_MOUSE_PAN = [xpos, ypos]


def mouse_button_callback(window, button, action, mods):
    global IS_MIDDLE_MOUSE_BUTTON_PRESSED
    global IS_RIGHT_MOUSE_BUTTON_PRESSED
    if button == glfw.MOUSE_BUTTON_MIDDLE:
        IS_MIDDLE_MOUSE_BUTTON_PRESSED = action == glfw.PRESS
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        IS_RIGHT_MOUSE_BUTTON_PRESSED = action == glfw.PRESS


def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def window_resize_callback(window, width, height):
    glViewport(0, 0, width, height)


def create_vao(vertices):
    points = np.array(vertices, dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, points.nbytes, points, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    return vao


def main(objects, window_width, window_height, window_title):
    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(window_width, window_height, window_title, None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_window_size_callback(window, window_resize_callback)

    glPointSize(4)

    for obj in objects:
        obj.set_shader()
        obj.vao = create_vao(vertices=obj.vertices)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        for obj in objects:
            glUseProgram(obj.shader)

            glBindVertexArray(obj.vao)

            transform = obj.transform_m
            transform = glm.translate(transform, glm.vec3(PAN[0], PAN[1], 0.0))
            transform = glm.scale(transform, glm.vec3(ZOOM, ZOOM, ZOOM))
            transform = glm.rotate(transform, ROTATION_ANGLE[0], glm.vec3(1.0, 0.0, 0.0))
            transform = glm.rotate(transform, ROTATION_ANGLE[1], glm.vec3(0.0, 1.0, 0.0))

            glUniformMatrix4fv(glGetUniformLocation(obj.shader, "transform"), 1, GL_FALSE, glm.value_ptr(transform))

            glDrawArrays(GL_POINTS, 0, len(obj.vertices) // 3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    object1 = Object(points_path='assets/go-gopher.obj', position_matrix=np.array([-0.5, 0.0, 0.0]), vertex_shader=vertex_shader, fragment_shader=fragment_shader1)
    object2 = Object(points_path='assets/go-gopher.obj', position_matrix=np.array([0.5, 0.0, 0.0]), vertex_shader=vertex_shader, fragment_shader=fragment_shader2)
    objects = [object1, object2]
    main(objects=objects, window_width=800, window_height=600, window_title="Hello world")

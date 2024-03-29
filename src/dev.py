from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import glm
import numpy as np

from utils.files import read_obj, read_shader_file
from utils.vao import create_vao, create_vao_sized
from utils.distance import calculate_distances, scale_distances, scale_distances_log


ZOOM = 1.0
PAN = [0.0, 0.0]
LAST_MOUSE_PAN = [0, 0]
IS_MIDDLE_MOUSE_BUTTON_PRESSED = False
IS_RIGHT_MOUSE_BUTTON_PRESSED = False
ROTATION_ANGLE = [0.0, 0.0]  # in radians
DYNAMIC_SPLAT_SIZING = False

def scroll_callback(window, x_offset, y_offset):
    global ZOOM
    ZOOM += y_offset * 0.1
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

def main():
    global ZOOM
    global PAN

    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1200, 1200, "Point Clouds", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_window_size_callback(window, window_resize_callback)

    if DYNAMIC_SPLAT_SIZING:
        vertex_shader_source = read_shader_file('shaders\dynamic_size.vert')
        geometry_shader_source = read_shader_file('shaders\dynamic_size_circle.geom')
    else:
        vertex_shader_source = read_shader_file('shaders\\base.vert')
        geometry_shader_source = read_shader_file('shaders\circle.geom')
    fragment_shader_source = read_shader_file('shaders\\base.frag')

    shader = compileProgram(
        compileShader(vertex_shader_source, GL_VERTEX_SHADER),
        compileShader(geometry_shader_source, GL_GEOMETRY_SHADER),
        compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    )

    vertices = read_obj('assets\go-gopher.obj') # You might have to tweak the slash as I am on Windows rn

    if DYNAMIC_SPLAT_SIZING:
        distances = calculate_distances(vertices)
        sizes = scale_distances_log(distances, 0.0005, 5.0)
        vao = create_vao_sized(vertices, sizes)
    else:
        vao = create_vao(vertices)

    glUseProgram(shader)

    size_location = glGetUniformLocation(shader, "size")
    glUniform1f(size_location, 0.01)  # Adjust size value as needed

    splat_color = np.array([0.41, 0.87, 0.98], dtype=np.float32)  # Example splat color
    transparency = 0.5  # Example transparency value
    luminance = 1.0 # Example luminance value

    glUniform3fv(glGetUniformLocation(shader, "splatColor"), 1, splat_color)
    glUniform1f(glGetUniformLocation(shader, "transparency"), transparency)
    glUniform1f(glGetUniformLocation(shader, "luminance"), luminance)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render
        glClearColor(0.3, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        transform = glm.mat4(1)  # Identity matrix
        transform = glm.translate(transform, glm.vec3(PAN[0], PAN[1], 0.0))
        transform = glm.scale(transform, glm.vec3(ZOOM, ZOOM, ZOOM))
        transform = glm.rotate(transform, ROTATION_ANGLE[0], glm.vec3(1.0, 0.0, 0.0))
        transform = glm.rotate(transform, ROTATION_ANGLE[1], glm.vec3(0.0, 1.0, 0.0))

        glUniformMatrix4fv(glGetUniformLocation(shader, "transform"), 1, GL_FALSE, glm.value_ptr(transform))

        glBindVertexArray(vao)
        glDrawArrays(GL_POINTS, 0, len(vertices)//3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

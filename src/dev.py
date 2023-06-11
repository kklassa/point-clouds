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

geometry_shader = """
#version 410
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;
uniform float size;
void main() {
    vec4 pos = gl_in[0].gl_Position;
    gl_Position = pos + vec4(-size, -size, 0.0, 0.0);
    EmitVertex();
    gl_Position = pos + vec4( size, -size, 0.0, 0.0);
    EmitVertex();
    gl_Position = pos + vec4(-size,  size, 0.0, 0.0);
    EmitVertex();
    gl_Position = pos + vec4( size,  size, 0.0, 0.0);
    EmitVertex();
    EndPrimitive();
}
"""

fragment_shader = """
#version 410 core

out vec4 fragColor;

uniform float transparency;
uniform float luminance;
uniform vec3 splatColor;

void main()
{
    vec3 finalColor = splatColor * luminance;
    float finalAlpha = transparency;
    fragColor = vec4(finalColor, finalAlpha);
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

def read_obj(filename):
    vertices = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if parts[0] == 'v':  # the line describes a vertex
                vertices.append(list(map(float, parts[1:])))

    return vertices

def main():
    global zoom
    global pan

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

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(geometry_shader, GL_GEOMETRY_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    vertices = read_obj('assets\go-gopher.obj') # You might have to tweak the slash as I am on Windows rn

    vao = create_vao(vertices)

    glUseProgram(shader)

    size_location = glGetUniformLocation(shader, "size")
    glUniform1f(size_location, 0.005)  # Adjust size value as needed

    splat_color = np.array([0.2, 0.0, 0.0], dtype=np.float32)  # Example splat color
    transparency = 0.5  # Example transparency value
    luminance = 0.8  # Example luminance value

    glUniform3fv(glGetUniformLocation(shader, "splatColor"), 1, splat_color)
    glUniform1f(glGetUniformLocation(shader, "transparency"), transparency)
    glUniform1f(glGetUniformLocation(shader, "luminance"), luminance)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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
        glDrawArrays(GL_POINTS, 0, len(vertices)//3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

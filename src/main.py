from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np

from globals import vertex_shader, fragment_shader
from object import Object


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


def main(translation_speed, rotation_speed, objects, window_width, window_height, window_title):
    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(window_width, window_height, window_title, None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    glPointSize(4)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader)

        for obj in objects:
            vao = create_vao(vertices=obj.vertices)
            glBindVertexArray(vao)

            rotate_x = 0.0
            rotate_y = 0.0

            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
                if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
                    rotate_x += rotation_speed  # Rotate up
                else:
                    obj.position_m[1] += translation_speed  # Move up

            if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
                if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
                    rotate_x -= rotation_speed  # Rotate down
                else:
                    obj.position_m[1] -= translation_speed  # Move down

            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
                if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
                    rotate_y += rotation_speed  # Rotate left
                else:
                    obj.position_m[0] -= translation_speed  # Move left

            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
                if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
                    rotate_y -= rotation_speed  # Rotate right
                else:
                    obj.position_m[0] += translation_speed  # Move right

            obj.rotation_m[0] = rotate_x
            obj.rotation_m[1] = rotate_y

            # Apply rotation
            rotation_matrix_x = np.array([
                [1, 0, 0, 0],
                [0, np.cos(np.radians(rotate_x)), -np.sin(np.radians(rotate_x)), 0],
                [0, np.sin(np.radians(rotate_x)), np.cos(np.radians(rotate_x)), 0],
                [0, 0, 0, 1]
            ], dtype=np.float32)

            rotation_matrix_y = np.array([
                [np.cos(np.radians(rotate_y)), 0, np.sin(np.radians(rotate_y)), 0],
                [0, 1, 0, 0],
                [-np.sin(np.radians(rotate_y)), 0, np.cos(np.radians(rotate_y)), 0],
                [0, 0, 0, 1]
            ], dtype=np.float32)

            # Apply transformations
            transform = np.matmul(rotation_matrix_x, obj.transform_m)
            transform = np.matmul(rotation_matrix_y, transform)
            transform[3, :3] = obj.position_m

            obj.transform_m = transform

            transformLoc = glGetUniformLocation(shader, "transform")
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, transform)

            glDrawArrays(GL_POINTS, 0, len(obj.vertices) // 3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    object1 = Object(points_path='assets/go-gopher.obj')
    object2 = Object(points_path='assets/go-gopher.obj', position_matrix=np.array([1.0, 1.0, 0.0]))
    objects = [object1, object2]
    main(translation_speed=0.05, rotation_speed=1.0, objects=objects, window_width=800, window_height=600, window_title="Hello world")

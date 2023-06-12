from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np
import random

from object_primitive import *
from transforms import *
from scene_object import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_NAME = 'window name'


def load_shader_from_file(path):
    with open(path, 'r') as f:
        return f.read()
    return None


def main():
    if not glfw.init():
        return

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME, None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader1 = compileProgram(
        compileShader(load_shader_from_file('shaders/default1.vert'), GL_VERTEX_SHADER),
        compileShader(load_shader_from_file('shaders/default1.frag'), GL_FRAGMENT_SHADER)
    )
    shader2 = compileProgram(
        compileShader(load_shader_from_file('shaders/default2.vert'), GL_VERTEX_SHADER),
        compileShader(load_shader_from_file('shaders/default2.frag'), GL_FRAGMENT_SHADER)
    )

    vertices1 = ObjectPrimitive.read_obj_file('assets/dense-figure.obj')
    vertices2 = ObjectPrimitive.read_obj_file('assets/go-gopher.obj')

    obj1 = ObjectPrimitive(vertices1)
    obj2 = ObjectPrimitive(vertices1)
    obj3 = ObjectPrimitive(vertices1)

    rotation_speed = 0.7
    rotate_x = 0.0
    rotate_y = 0.0

    s_obj1 = SceneObject('s_obj1', obj1, Transforms.identity())

    s_obj2 = SceneObject('s_obj2', obj2, Transforms.identity())
    s_obj2.transform(Transforms.rotate(np.radians(90), np.radians(0), np.radians(0)))
    s_obj2.transform(Transforms.translate(0.0, -0.4, 0.4))

    s_obj3 = SceneObject('s_obj3', obj3, Transforms.identity())
    s_obj3.transform(Transforms.translate(0.0, -0.8, 0.8))

    s_obj1.add_child(s_obj2)
    s_obj2.add_child(s_obj3)

    while not glfw.window_should_close(window):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            rotate_x += rotation_speed
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            rotate_x -= rotation_speed
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            rotate_y += rotation_speed
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            rotate_y -= rotation_speed

        view_transform = Transforms.rotate(np.radians(rotate_x), np.radians(rotate_y), np.radians(0))
        s_obj2.transform(view_transform)

        s_obj1.draw(shader1, 5)
        s_obj2.draw(shader2, 3)
        s_obj3.draw(shader1, 3)

        s_obj2.transform(np.linalg.inv(view_transform))

        glfw.swap_buffers(window)
        glfw.poll_events()

        
    glfw.terminate()

if __name__ == '__main__':
    main()

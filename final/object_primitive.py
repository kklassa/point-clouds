from OpenGL.GL import *
import glfw
import numpy as np


class ObjectPrimitive:
    @staticmethod
    def read_obj_file(path):
        with open(path, 'r') as f:
            return np.array(list(map(lambda x: np.array(list(map(float, x[1:]))), filter(lambda x: x[0] == 'v', map(lambda x: x.split(), f.readlines())))))
        return None

    def _create_vao(self, vertices):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        vertices = np.array(vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    def __init__(self, vertices):
        self.vertices = vertices
        self._create_vao(self.vertices)

    def draw(self, transform, shader, points_size):
        glUseProgram(shader)
        glPointSize(points_size)
        transformLoc = glGetUniformLocation(shader, 'transform')
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, transform)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, len(self.vertices)//3)

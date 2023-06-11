from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


class Object:
    def __init__(self, points_path, position_matrix=None, rotation_matrix=None, vertex_shader=None, fragment_shader=None, geometry_shader=None):
        self.points_path = points_path
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.geometry_shader = geometry_shader

        self.position_m = position_matrix if position_matrix is not None else np.array([0.0, 0.0, 0.0])
        self.rotation_m = rotation_matrix if rotation_matrix is not None else np.array([0.0, 0.0])

        self.transform_m = self.create_transform_m()
        self.vertices = self.read_obj()


    def set_shader(self):
        if self.geometry_shader:
            shader = compileProgram(
            compileShader(self.vertex_shader, GL_VERTEX_SHADER),
            compileShader(self.fragment_shader, GL_FRAGMENT_SHADER),
            compileShader(self.geometry_shader, GL_GEOMETRY_SHADER)
        )
        else:
            shader = compileProgram(
                compileShader(self.vertex_shader, GL_VERTEX_SHADER),
                compileShader(self.fragment_shader, GL_FRAGMENT_SHADER)
            )
        self.shader = shader


    def read_obj(self):
        vertices = []

        with open(self.points_path, 'r') as file:
            for line in file:
                parts = line.split()
                if parts[0] == 'v':  # the line describes a vertex
                    vertices.append(list(map(float, parts[1:])))

        return vertices
    
    
    def create_transform_m(self):
        transform = np.identity(4, dtype=np.float32)
        transform[3, :3] = self.position_m

        return transform
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from utils.files import read_shader_file
import glm


class Object:
    def __init__(self, points_path, position_matrix=None, rotation_matrix=None, luminance=0, transparency=0, splat_color=None):
        self.points_path = points_path

        self.position_m = position_matrix if position_matrix is not None else np.array([0.0, 0.0, 0.0])
        self.rotation_m = rotation_matrix if rotation_matrix is not None else np.array([0.0, 0.0])

        self.luminance = luminance
        self.transparency = transparency
        self.splat_color = splat_color

        self.transform_m = self.create_transform_m()
        self.vertices = self.read_obj()
        self.vao = None


    def set_shader(self, dynamic_splat_sizing=False):
        if dynamic_splat_sizing:
            vertex_shader = read_shader_file('shaders/dynamic_size.vert')
            geometry_shader = read_shader_file('shaders/dynamic_size_circle.geom')
        else:
            vertex_shader = read_shader_file('shaders/base.vert')
            geometry_shader = read_shader_file('shaders/circle.geom')
        fragment_shader = read_shader_file('shaders/base.frag')

        shader = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER),
            compileShader(geometry_shader, GL_GEOMETRY_SHADER)
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
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(self.position_m[0], self.position_m[1], self.position_m[2]))
        return transform
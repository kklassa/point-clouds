import numpy as np
import copy


class SceneObject:
    names = set()

    def __init__(self, name, object_primitive, transformations):
        if name in type(self).names:
            raise Exception('Existing name of SceneObject object')

        self.name = name
        type(self).names.add(name)
        self.object_primitive = object_primitive
        self.transformations = transformations

        self.children = []

    def add_child(self, child):
        self.children += [child]

    def transform(self, transformation):
        for child in self.children:
            child.transform(transformation)

        # self.transformations = np.linalg.inv(center)@self.transformations
        # self.transformations = transformation@self.transformations
        # self.transformations = (transformation@center)@self.transformations

        new_transformations = np.identity(4)
        new_transformations = transformation@new_transformations
        new_transformations = self.transformations@new_transformations
        self.transformations = new_transformations

    def draw(self, shader, points_size):
        self.object_primitive.draw(self.transformations, shader, points_size)

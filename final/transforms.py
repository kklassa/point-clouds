import numpy as np


class Transforms:
    @staticmethod
    def identity():
        return np.identity(4)

    @staticmethod
    def translate(x, y, z):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1]
        ])

    @staticmethod
    def scale(x, y, z):
        return np.array([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotate(x, y, z):
        return np.array([
            [1, 0, 0, 0],
            [0, np.cos(x), -np.sin(x), 0],
            [0, np.sin(x), np.cos(x), 0],
            [0, 0, 0, 1]
        ])@np.array([
            [np.cos(y), 0, np.sin(y), 0],
            [0, 1, 0, 0],
            [-np.sin(y), 0, np.cos(y), 0],
            [0, 0, 0, 1]
        ])@np.array([
            [np.cos(z), -np.sin(z), 0, 0],
            [np.sin(z), np.cos(z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

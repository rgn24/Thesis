import numpy as np

class Reservoir:
    def __init__(self, height: float = 1.1, width: float = 1.1, offset: float = 0.0):
        self.height = height
        self.width = width
        self.offset = offset
        self.vertices = self.get_vertices()


    def get_vertices(self):
        x_start = 0.0 + self.offset
        x_wedge = np.linspace(x_start, x_start + self.width, 2)
        vertices = np.array([[x_wedge[0], 0.0],
                             [x_wedge[0], self.height],
                             [x_wedge[-1], 0],
                             [x_wedge[-1], self.height]])
        return vertices

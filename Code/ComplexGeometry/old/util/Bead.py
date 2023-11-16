import numpy as np
import matplotlib.pyplot as plt


class Bead:
    def __init__(self, outer_diameter: float = 7.0, inner_Diameter: float = 4.0, angle: float = 5.0, fraction: float = 0.5, offset: float = 1.0):
        self.r_o = outer_diameter / 2
        self.r_i = inner_Diameter / 2
        self.angle = angle
        self.fraction = fraction
        self.dx_R, self.length_segment = self.get_dxR()
        self.n_points = 20
        self.offset = offset

        x_steps = np.linspace(-self.dx_R, self.length_segment - self.dx_R, self.n_points)
        self.x_wedge, self.z_R = self.get_zR(x_steps)
        self.vertices = self.get_vertices()

    def get_dxR(self) -> np.float64:
        dx_r = np.sqrt(1 - np.power((self.r_i / self.r_o), 2)) * self.r_o
        len_x_fraction = 2 * dx_r * self.fraction
        return dx_r, len_x_fraction

    def get_length_segment(self):
        return self.dx_R * 2

    def get_zR(self, series):
        """
        The get_zR function takes a series of x values and returns the corresponding z values.
        The function uses the equation for a circle to calculate z_R, which is then added to dx_R
        to get the final value of z.

        :param self: Refer to the class instance
        :param series: Create the x-axis of the graph
        :return: The x-coordinates and z-coordinates of the right boundary
        """
        z_R = np.sqrt(1 - (np.power(series / self.r_o, 2))) * self.r_o
        return series + self.dx_R + self.offset, z_R



    def get_vertices(self):

        vertices = np.array([[self.x_wedge[0], 0.0],
                             [self.x_wedge[0], self.z_R[0]],
                             [self.x_wedge[-1], 0.0],
                             [self.x_wedge[-1], self.z_R[-1]]])
        return vertices

    def get_maxima(self):
        return [self.length_segment, self.r_o]

    def visualize(self):
        """
        The visualize function plots the wedge and its radius of curvature.
        :param self: Represent the instance of the class
        :return: A plot of the wedge and the r-curve
        :doc-author: Trelent
        """
        plt.plot(self.x_wedge, self.z_R)
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        plt.grid()
        plt.show()

from copy import deepcopy
import numpy as np

from util.Bead import *
from util.Joint import *
from util.Reservoir import *


class ComplexGeometry2D:
    def __init__(self, n_Segments: float = 1.0, add_reservoir: bool = False, width_joint=0.1):
        #TODO add inputs for Bead and joint!!
        self.n_segments = n_Segments
        self.add_reservoir = add_reservoir
        self.width_joint = width_joint

        self.vertices = self.construct_2D_Wedge()

    def get_number_of_vertices_2D(self):
        # for now always more than one element is assumed!
        ##if self.n_segments <= 1.0:
        ##    print("helo")
        ##    no_joint = 2
        ##else:
        ##    no_joint = 0
        return (np.ceil(self.n_segments)) * 4 + self.add_reservoir*2

    def construct_2D_Wedge(self):
        offset = 0.0
        n_verts = self.get_number_of_vertices_2D()
        vertices = np.zeros((int(n_verts), 2))
        upper_itt_lim = int(np.ceil(self.n_segments)-1) # TODO gets zero, if n_segments == 1 maybe pull init out
        for i in range(upper_itt_lim):
            bead = Bead(fraction=1.0, offset=offset)
            offset += bead.length_segment
            joint = Joint(height=bead.vertices[-1, 1], width=self.width_joint, offset=offset)
            offset += self.width_joint
            # first element
            if i == 0:
                vertices[0:4, :] = bead.vertices
                if self.n_segments <= 1:
                    continue
                else:
                    vertices[4:6, :] = joint.vertices[-2:, :]
            else:
                vertices[i * 6:2 * i + 6, :] = bead.vertices[-2:, :]
                vertices[i * 8:2 * i + 8, :] = joint.vertices[-2:, :]
        frac = self.n_segments-upper_itt_lim
        bead = Bead(fraction=frac, offset=offset)
        vertices[-2:, :] = bead.vertices[-2:, :]
        if self.add_reservoir:
            reservoir = Reservoir
        return vertices

    def return_values(self):
        """returns the vertices of the wedge and the maxima of the wedge, the maxima of a half wedge, the length of the joint and the number of segments

        Returns:
            list: list of relevant values to construct the wedge
        """
        bead10 = Bead(fraction=1.0)
        bead05 = Bead(fraction=.5)
        return [self.vertices, bead10.get_maxima(), bead05.get_maxima(), self.width_joint, self.n_segments]

    def visualize(self):
        """
        The visualize function plots the wedge and its radius of curvature.
        :param self: Represent the instance of the class
        :return: A plot of the wedge and the r-curve
        :doc-author: Trelent
        """
        plt.scatter(self.vertices[:, 0], self.vertices[:, 1])
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        plt.grid()
        plt.show()

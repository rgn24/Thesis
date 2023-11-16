import numpy as np
from util.util_functions import *

class Bead:
    def __init__(self, angle: float = 5.0, outer_diameter: float = 7.0, inner_Diameter: float = 4.0):
        self.r_o = outer_diameter / 2
        self.r_i = inner_Diameter / 2
        self.angle = angle
        self.length_segment = 0
        self.dx_R = 0
        self.z_R = 0
        self.verts_2D = None
        self.verts_3D = None
        
        self.set_len_x()
        self.set_zR()
        
        
    def set_len_x(self) -> None:
        self.dx_R = np.sqrt(1 - np.power((self.r_i / self.r_o), 2)) * self.r_o
        print("dxr", type(self.dx_R))
        self.length_segment = np.dot(2, self.dx_R)
        print("length", self.length_segment)
    
    def set_zR(self):
        """
        The get_zR function takes a series of x values and returns the corresponding z values.
        The function uses the equation for a circle to calculate z_R, which is then added to dx_R
        to get the final value of z.

        :param self: Refer to the class instance
        :param series: Create the x-axis of the graph
        :return: The x-coordinates and z-coordinates of the right boundary
        """
        series = np.array([self.dx_R, 0])
        print("dxRRR", self.dx_R)
        self.z_R = np.sqrt(1 - (np.power(series / self.r_o, 2))) * self.r_o
        print("DZR", self.z_R)
        
    
    def generate_verts2D(self):
        # vertices = [[]]
        print(self.length_segment)
        vertices = np.array([[0, 0.0],
                             [0, self.z_R[0]],
                             [self.length_segment, 0.0],
                             [self.length_segment, self.z_R[-1]]])
        print(vertices)
        #return vertices

    def get_maxima(self):
        return [self.length_segment, self.r_o]
    
    def generate_verts3D(self):
        y_wedge, z_wedge = wedify(self.z_R, self.angle)
    
if __name__== "__main__":
    bead = Bead()
    bead.generate_verts2D()
    bead.generate_verts3D()
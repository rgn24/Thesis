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
        self.verts_3D = np.zeros([3,8])
        
        self.connection_y = 0
        self.connection_z = 0
        
        self.max_y = 0
        self.max_z = 0
        
        self.set_len_x()
        self.set_zR()
        
    def get_info(self):
        info = {"Bead length":self.length_segment, 
                "inner Radius": self.r_i, 
                "outer Radius": self.r_o, 
                "Extrema y-Koordinate": self.max_y,
                "Extrema z-Koordinate": self.max_z,
                "Connector y-Koordinate": self.connection_y,
                "Connector z-Koordinate": self.connection_z}
        return info
        
    def print_info(self):
        print("\nInfo:")
        info = self.get_info()
        for key in info.keys():
            print(key, ": ", info[key])
        
        
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
        print("vertieces: \n", vertices)
        #return vertices

    def get_maxima(self):
        return [self.length_segment, self.r_o]
    
    def generate_verts3D(self):
        y_wedge, z_wedge = wedify(self.z_R, self.angle)
        self.connection_y = y_wedge[0]
        self.max_y = y_wedge[1]
        self.connection_z = z_wedge[0]
        self.max_z = z_wedge[1]
        self.verts_3D[:, 0] = np.array([0,0,0])
        self.verts_3D[:, 1] = np.array([0,self.connection_y,self.connection_z])
        self.verts_3D[:, 2] = np.array([0,-self.connection_y,self.connection_z])
        #print(self.verts_3D)
        #print(self.verts_3D.shape)
        
    def get_block_verts_id(self):
        return [0, 1, 2, 0, 3, 4, 5, 3]
    
def update_vertices(x_off, y_conn, z_conn):
    vertices = np.array([[x_off, 0, 0],
                         [x_off, y_conn, z_conn],
                         [x_off, -y_conn, z_conn]])
    
    vert_body= lambda vert : f"\t({vert[0]} {vert[1]} {vert[2]})\n"
    verts_blockMesh = ""
    for row in vertices:
        verts_blockMesh += vert_body(row)
    return verts_blockMesh

def update_blocks(number_of_elements:list, block_id):
    blocks_template = np.array([0, 1, 2, 0, 3, 4, 5, 3])
    offset_id = block_id * 3
    blocks = blocks_template + offset_id
    blocks_body = lambda blocks, number_of_elements : f"\t({blocks[0]} {blocks[1]} {blocks[2]} {blocks[3]} {blocks[4]} {blocks[5]} {blocks[6]} {blocks[7]}) ({number_of_elements[0]} {number_of_elements[1]} {number_of_elements[2]}) simpleGrading (1 1 1)"
    return blocks_body(blocks, number_of_elements)

def update_edges(block_id, x_mid:float, y_max:float, z_max:float):
    arc_template_pos = np.array([1, 4])
    arc_template_neg = np.array([2, 5]) 
    offset_id = block_id * 6
    arc_neg = arc_template_neg + offset_id
    arc_pos = arc_template_pos + offset_id
    edges_pos = lambda arc_pos, x_mid, y_max, z_max : f"\tarc({arc_pos[0]} {arc_pos[1]}) ({x_mid} {y_max} {z_max}))"
    edges_neg = lambda arc_neg, x_mid, y_max, z_max : f"\tarc({arc_neg[0]} {arc_neg[1]}) ({x_mid} {-y_max} {z_max}))"
    return f"{edges_pos(arc_pos, x_mid, y_max, z_max)}\n{edges_neg(arc_neg, x_mid, y_max, z_max)}"

def update_faces(block_id):
    offset_id = block_id * 3
    wall_template = np.array([1, 4, 5, 2])
    front_template = np.array([0, 3, 4, 1])
    back_template = np.array([0, 2, 5, 3])
    wall_id = wall_template + offset_id
    front_id = front_template + offset_id
    back_id = back_template + offset_id
    wall = lambda wall_id : f"\t({wall_id[0]} {wall_id[1]} {wall_id[2]} {wall_id[3]})"
    front = lambda front_id : f"\t({front_id[0]} {front_id[1]} {front_id[2]} {front_id[3]})"
    back = lambda back_id : f"\t({back_id[0]} {back_id[1]} {back_id[2]} {back_id[3]})"
    return wall, front, back

def get_header():
    pass
    #TODO Add head
    return head

def get_transform():
    pass
    #TODO Add transform
    return transform

def add_header(verts, blocks, edges, faces):
    verts += "\nvertecies(\n"
    blocks += "\nblocks(\n"
    edges += "\nedges(\n"
    faces += "\nfaces(\n"
    #TODO Add header
    return verts, blocks, edges, faces

if __name__== "__main__":
    number_of_beads = 2
    bead = Bead()
    bead.generate_verts2D()
    bead.generate_verts3D()
    bead.print_info()
    
    
    
    #print(update_vertices(0, 1, 2))
    #print(update_blocks(bead.get_block_verts_id(), [1,2,3]))
    
    offset = 0
    layers = number_of_beads * 2 + 1
    count_block = 0
    offset = 0
    
    vertices_blockMesh = ""
    blocks_blockMesh = ""
    edges_blockMesh = ""
    faces_blockMesh = ""
    vertices_blockMesh, blocks_blockMesh, edges_blockMesh, faces_blockMesh = add_header(vertices_blockMesh, blocks_blockMesh, edges_blockMesh, faces_blockMesh)
    for i in range(layers):
        if i%2 == 0 and i != 0:
            count_block += 1
            offset += 1
        elif i%2 != 0 and i != 0:
            offset += bead.length_segment
        vertices_blockMesh += update_vertices(offset, bead.connection_y, bead.connection_z)
    wall, front, back = "", "", ""
    for i in range(number_of_beads * 2):
        if i%2 == 0:
            blocks_blockMesh += update_blocks([1,1,1], i)
        elif i%2 != 0 and i != 0:
            blocks_blockMesh += update_blocks([10,10,10], i)
            edges_blockMesh += update_edges(i, bead.length_segment/2, bead.max_y, bead.max_z)


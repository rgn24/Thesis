import numpy as np
from util.util_functions import *
import os

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
    
    
    
class BlockMesh:
    def __init__(self, n_beads:int,convert:str, geom:list, xyz_resolution:list) -> None:
        self.n_beads = n_beads
        self.geom = geom
        self.xyz_resolution = xyz_resolution
        self.convert = convert
        
        # internal variables
        self.layers = self.n_beads * 2 + 1
        self.vertices_blockMesh = ""
        self.blocks_blockMesh = ""
        self.edges_blockMesh = ""
        self.faces_blockMesh = ""
        self.blockMesh = ""
        self.y_conn = self.geom[0]
        self.z_conn = self.geom[1]
        self.y_max = self.geom[2]
        self.z_max = self.geom[3]
        self.length_segment = geom[4]
        self.joint_width = self.length_segment / self.xyz_resolution[0]
        
        # temp internal variables faces
        self.wall = "\twall\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n"
        self.front = "\tfront\n\t{\n\t\ttype wedge;\n\t\tfaces\n\t\t(\n"
        self.back = "\tback\n\t{\n\t\ttype wedge;\n\t\tfaces\n\t\t(\n"
        self.axis = "\taxis\n\t{\n\t\ttype axis;\n\t\tfaces\n\t\t(\n"
        self.top = "\ttop\n\t{\n\t\ttype empty;\n\t\tfaces\n\t\t(\n"
        self.bottom = "\tbottom\n\t{\n\t\ttype empty;\n\t\tfaces\n\t\t(\n"
        
    def add_header(self):
        self.vertices_blockMesh += "\nvertices\n(\n"
        self.blocks_blockMesh += "\nblocks\n(\n"
        self.edges_blockMesh += "\nedges\n(\n"
        self.faces_blockMesh += "\nboundary\n(\n"
        #TODO Add header
        
    def add_end(self):
        self.vertices_blockMesh += ");\n"
        self.blocks_blockMesh += ");\n"
        self.edges_blockMesh += ");\n"
        self.faces_blockMesh += ");\n"
        
    def add_end_faces(self):
        self.wall += "\t\t);\n\t}\n"
        self.front += "\t\t);\n\t}\n"
        self.back += "\t\t);\n\t}\n"
        self.axis += "\t\t);\n\t}\n"
        self.top += "\t\t);\n\t}\n"
        self.bottom += "\t\t);\n\t}\n"
        
    def add_header_blockMesh(self):
        head = [
            r"/*--------------------------------*- C++ -*----------------------------------*\ ",
            r"| =========                 |                                                 | ",
            r"| \\      /  F ield         | foam-extend: Open Source CFD                    | ",
            r"|  \\    /   O peration     | Version:     5.0                                | ",
            r"|   \\  /    A nd           | Web:         http://www.foam-extend.org         | ",
            r"|    \\/     M anipulation  | For copyright notice see file Copyright         | ",
            r"\*---------------------------------------------------------------------------*/ ",
            r"FoamFile ",
            r"{ ",
            r"	version     2.0; ",
            r"	format      ascii; ",
            r"	class       dictionary; ",
            r"	object      blockMeshDict; ",
            r"} ",
            r"// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // ",
            "\n",
            f"convertToMeters {self.convert};",
            "\n"
        ]
        text = ""
        # convert to string
        for line in head:
            text += line + "\n"
        self.blockMesh = text
        
    def update_vertices(self, x_off):
        # generate vertices
        vertices = np.array([[x_off, 0, 0],
                            [x_off, self.y_conn, self.z_conn],
                            [x_off, -self.y_conn, self.z_conn]])
        # function to update string
        vert_body= lambda vert : f"\t({vert[0]} {vert[1]} {vert[2]})\n"
        verts_blockMesh = ""
        for row in vertices:
            verts_blockMesh += vert_body(row)
        # update vertices
        self.vertices_blockMesh += verts_blockMesh
        
    def update_blocks(self, block_id, number_of_elements:list):
        #templates
        blocks_template = np.array([0, 1, 2, 0, 3, 4, 5, 3])
        #update ids
        offset_id = block_id * 3
        blocks = blocks_template + offset_id
        #functions
        blocks_body = lambda blocks, number_of_elements : f"\thex ({blocks[0]} {blocks[1]} {blocks[2]} {blocks[3]} {blocks[4]} {blocks[5]} {blocks[6]} {blocks[7]}) ({number_of_elements[0]} {number_of_elements[1]} {number_of_elements[2]}) simpleGrading (1 1 1)\n"
        # update blocks
        self.blocks_blockMesh += blocks_body(blocks, number_of_elements)
        
    def update_edges(self, block_id, x_mid:float):
        #templates
        arc_template_pos = np.array([1, 4])
        arc_template_neg = np.array([2, 5])
        #update ids
        offset_id = block_id * 3
        arc_neg = arc_template_neg + offset_id
        arc_pos = arc_template_pos + offset_id
        #functions
        edges_pos = lambda arc_pos, x_mid, y_max, z_max : f"\tarc {arc_pos[0]} {arc_pos[1]} ({x_mid} {y_max} {z_max})\n"
        edges_neg = lambda arc_neg, x_mid, y_max, z_max : f"\tarc {arc_neg[0]} {arc_neg[1]} ({x_mid} {-y_max} {z_max})\n"
        # update edges
        self.edges_blockMesh += f"{edges_pos(arc_pos, x_mid, self.y_max, self.z_max)}{edges_neg(arc_neg, x_mid, self.y_max, self.z_max)}"
        
    def update_faces(self, block_id):
        #templates
        wall_template = np.array([1, 4, 5, 2])
        front_template = np.array([0, 3, 4, 1])
        back_template = np.array([0, 2, 5, 3])
        axis_template = np.array([0, 3 , 3, 0])
        #update ids
        offset_id = block_id * 3
        wall_id = wall_template + offset_id
        front_id = front_template + offset_id
        back_id = back_template + offset_id
        axis_id = axis_template + offset_id
        #functions
        l_wall = lambda wall_id : f"\t\t\t({wall_id[0]} {wall_id[1]} {wall_id[2]} {wall_id[3]})\n"
        l_front = lambda front_id : f"\t\t\t({front_id[0]} {front_id[1]} {front_id[2]} {front_id[3]})\n"
        l_back = lambda back_id : f"\t\t\t({back_id[0]} {back_id[1]} {back_id[2]} {back_id[3]})\n"
        l_axis = lambda axis_id : f"\t\t\t({axis_id[0]} {axis_id[1]} {axis_id[2]} {axis_id[3]})\n"
        # update faces
        self.wall += l_wall(wall_id)
        self.front += l_front(front_id)
        self.back += l_back(back_id)
        self.axis += l_axis(axis_id)
        
    def merge_faces(self):
        template_bottom = np.array([0, 1, 2, 0])
        template_top = template_bottom + self.n_beads * 6
        self.top += f"\t\t\t({template_top[0]} {template_top[1]} {template_top[2]} {template_top[3]})\n"
        self.bottom += f"\t\t\t({template_bottom[0]} {template_bottom[1]} {template_bottom[2]} {template_bottom[3]})\n"
        self.add_end_faces()
        
        self.faces_blockMesh += f"{self.wall}\n{self.front}\n{self.back}\n{self.axis}\n{self.top}\n{self.bottom}\n"
    
    
    def generate_block_mesh_dict(self):
        offset = 0
        self.add_header()
        
        # vertices iterations
        for i in range(self.layers):
            if i%2 == 0 and i != 0:
                offset += self.joint_width
            elif i%2 != 0 and i != 0:
                offset += self.length_segment
            self.update_vertices(offset)
        # block iterations
        offset = 0
        for i in range(self.n_beads * 2):
            if i%2 == 0:
                self.update_blocks(i, [self.xyz_resolution[2], self.xyz_resolution[1], self.xyz_resolution[0]])
                self.update_edges(i, offset + self.length_segment/2)
                offset += self.length_segment
            elif i%2 != 0 :
                self.update_blocks(i, [self.xyz_resolution[2], self.xyz_resolution[1], 1])
                offset += self.joint_width
            
            self.update_faces(i)
            
        self.merge_faces()
        self.add_end()
        self.add_header_blockMesh()
        self.blockMesh += self.vertices_blockMesh + self.blocks_blockMesh + self.edges_blockMesh + self.faces_blockMesh + "\nmergePatchPairs\n(\n);\n"
        
        print(self.blockMesh)
        
    def save_blockMeshDict(self, path=os.getcwd()+"\\blockMeshDict"):
        with open(path, "w") as f:
            f.write(self.blockMesh)
        print(f"blockMeshDict saved in {path}")

if __name__== "__main__":
    number_of_beads = 2
    bead = Bead()
    bead.generate_verts2D()
    bead.generate_verts3D()
    bead.print_info()
    
    blockmesh = BlockMesh(2, "1e-9",[bead.connection_y, bead.connection_z, bead.max_y, bead.max_z, bead.length_segment], [10,1,10])
    blockmesh.generate_block_mesh_dict()
    blockmesh.save_blockMeshDict()
    
    #print(update_vertices(0, 1, 2))
    #print(update_blocks(bead.get_block_verts_id(), [1,2,3]))
    
    

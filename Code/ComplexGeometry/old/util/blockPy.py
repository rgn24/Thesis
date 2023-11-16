from util.twoDGeom import *

class BlockPy:
    def __init__(self, geom: list, reservoir: bool= False, angle: float=5.0):
        self.vertices2D = geom[0]
        self.maxima = geom[2]
        self.width_joint = geom[3]
        self.n_segments = geom[4]
        self.reservoir = reservoir
        self.angle = angle
        self.vertices3D = self.generate_verts3D()
        print(self.vertices3D)


    def generate_verts3D(self):
        n_verts = np.shape(self.vertices2D)[0] + int(np.shape(self.vertices2D)[0]/2)
        vertices3D = np.zeros([n_verts, 3])

        curr_3D = 0
        for id_vert, vert in enumerate(self.vertices2D):

            if id_vert % 2 == 0:
                vertices3D[curr_3D, 0] = self.vertices2D[id_vert, 0]
                curr_3D += 1
            else:
                vertices3D[curr_3D, 0] = self.vertices2D[id_vert, 0]
                vertices3D[curr_3D, 2] = self.vertices2D[id_vert, 1]
                curr_3D += 1
                vertices3D[curr_3D, 0] = self.vertices2D[id_vert, 0]
                vertices3D[curr_3D, 2] = self.vertices2D[id_vert, 1]
                curr_3D += 1
        vertices3D[:, 1], vertices3D[:, 2] = self.wedify(vertices3D[:, 2])
        # convertion to nescessary negative values for y
        for id_vert, vert in enumerate(vertices3D):
            if (id_vert + 1) % 3 == 0:
                vertices3D[id_vert, 1] *= -1

        return vertices3D

    def wedify(self, z: np.array) -> np.array:

        print(np.cos(np.deg2rad(self.angle / 2)))
        z_wedge = z * np.cos(np.deg2rad(self.angle / 2))
        y_wedge = z * np.sin(np.deg2rad(self.angle / 2))
        print(f"y: {y_wedge}, z: {z_wedge}")
        return y_wedge, z_wedge

    def blockMesh_header(self):
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
            "convertToMeters 1e-09;",
            "\n"
        ]
        text = ""
        # convert to string
        for line in head:
            text += line + "\n"
        return text

    def blockMesh_vertices(self):
        text = "\nvertices\n(\n"
        count = 0
        for vert in self.vertices3D:
            text += f"\t({vert[0]} {vert[1]} {vert[2]})\t//Vert {count}\n"
            count += 1
        text += ");"
        return text

    def blockMesh_edges(self):
        text = "\nedges\n(\n"
        max_y, max_z = self.wedify(self.maxima[1])
        # get start and offset of the arc for each block
        x = self.maxima[0]
        dx = self.maxima[0] * 2 + self.width_joint
        n_blocks = int(self.n_segments)
        for i in range(n_blocks):
            text += f"\tarc {1 + 6 * i} {4 + 6 * i} ({x + dx * i} {max_y} {max_z})\n"
            text += f"\tarc {2 + 6 * i} {5 + 6 * i} ({x + dx * i} {-max_y} {max_z})\n"
        text += ");\n"
        return text

    def blockMesh_blocks(self, n_elems=[10, 1, 10]):

        b_blocks = "\nblocks\n(\n"
        n_blocks = int(self.n_segments * 2)
        reservoir_elems = int(self.vertices2D[-1,0] * 0.25 * 4)
        for i in range(n_blocks):
            if i % 2 == 0 and i != n_blocks-2:
                b_blocks += f"\thex ({0 + i * 3} {1 + i * 3} {2 + i * 3} {0 + i * 3} {3 + i * 3} {4 + i * 3} {5 + i * 3} {3 + i * 3}) ({n_elems[2]} {n_elems[1]} {n_elems[0]}) simpleGrading (1 1 1)\n"
            elif (i % 2 == 0 and i == n_blocks - 2):
                b_blocks += f"\thex ({0 + i * 3} {1 + i * 3} {2 + i * 3} {0 + i * 3} {3 + i * 3} {4 + i * 3} {5 + i * 3} {3 + i * 3}) ({n_elems[2]} 1 {n_elems[0]}) simpleGrading (1 1 1)\n"
            elif(i != n_blocks-1):
                b_blocks += f"\thex ({0 + i * 3} {1 + i * 3} {2 + i * 3} {0 + i * 3} {3 + i * 3} {4 + i * 3} {5 + i * 3} {3 + i * 3}) ({n_elems[2]} 1 1) simpleGrading (1 1 1)\n"
            else:
                continue
        if self.reservoir:
            # add due to reservoir
            b_blocks += f"\thex ({0 + n_blocks * 3} {1 + n_blocks * 3} {2 + n_blocks * 3} {0 + n_blocks * 3} {3 + n_blocks * 3} {4 + n_blocks * 3} {5 + n_blocks * 3} {3 + n_blocks * 3}) ({n_elems[2]} {n_elems[1]} {reservoir_elems}) simpleGrading (1 1 1)\n"
            b_blocks += f"\thex ({2 + n_blocks * 3} {5 + n_blocks * 3} {4 + n_blocks * 3} {1 + n_blocks * 3} {7 + n_blocks * 3} {9 + n_blocks * 3} {8 + n_blocks * 3} {6 + n_blocks * 3}) ({reservoir_elems} {n_elems[1]} {2 * n_elems[2]}) edgeGrading (1 1 1 1 1 1 1 1 2 2 2 2)\n"
        b_blocks += ");\n"
        return b_blocks
    
    def blockMesh_faces(self):
        print(self.vertices3D)
        front = lambda s: f"\t\t\t({s[0]}\t{s[1]}\t{s[2]}\t{s[3]}\t)\n"
        n_blocks = int(self.n_segments * 2)
        print(n_blocks, self.n_segments)


from util.twoDGeom import ComplexGeometry2D
from util.blockPy import BlockPy

elem = ComplexGeometry2D(add_reservoir=False, n_Segments=5.0)
blockpy = BlockPy(geom=elem.return_values())
#print(blockpy.blockMesh_header())
#print(blockpy.blockMesh_vertices())
print(blockpy.blockMesh_blocks())
#print(blockpy.blockMesh_edges())
#print(blockpy.blockMesh_faces())
blockpy.blockMesh_faces()
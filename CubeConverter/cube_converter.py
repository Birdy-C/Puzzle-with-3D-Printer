bl_info = {
    "name": "New Object",
    "author": "Birdy",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Prepare a cube structure for 3D printer",
    "warning": "",
    "doc_url": "https://github.com/Birdy-C/Puzzle-with-3D-Printer/tree/main/CubeConverter",
    "category": "Add Mesh",
}


import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import FloatProperty, StringProperty, BoolProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import numpy as np

import io

def translate(mesh, offsetX):
    from mathutils import Matrix
    matrix = Matrix.Translation((offsetX, 0, 0))
    mesh.transform(matrix)
    mesh.update()
    

def parse_cube_data(data):
    s1 = data.split('\n');
    s2 = [t0.split('\t') for t0 in s1]
    s3 = [[t1.split(',') for t1 in t0] for t0 in s2]
    cubic_array = np.array(s3).astype(np.int)
    return cubic_array

def read_cube_data(context, filepath):
    print("running read_some_data...")
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    
    data = "\n".join(data.splitlines())
    s = data.split("\n#\n");
    
    cubic_array = []
    for single_info in s:
        cubic_array.append(parse_cube_data(single_info))
    print(cubic_array)
    return cubic_array

def is_taken(cubic_info, ix, iy, iz):
    (x,y,z) = cubic_info.shape
    if(ix < 0 or iy < 0 or iz < 0):
        return False
    if(ix >= x or iy >= y or iz >= z):
        return False;
    return cubic_info[ix][iy][iz] > 0
    
def draw_cube(self, context, cubic_info, offsetX):

    ## data for final import    
    verts = []

    edges = [] # empty
    faces = []
    
    
    ## handle
    link_fulllength = self.extend_percent + 1
    t_points = [
            Vector((0, 0, 0)),
            Vector((0, 0, 1)),
            Vector((0, 1, 1)),
            Vector((0, 1, 0)),
            Vector((1, 0, 0)),
            Vector((1, 0, 1)),
            Vector((1, 1, 1)),
            Vector((1, 1, 0)),
        ]
    t_faceindex = [[0,1,2,3],[5,4,7,6],[1,0,4,5],[3,2,6,7],[0,3,7,4],[2,1,5,6]] # x y z
    t_faceindex_inverse = [[0,1,2,3],[4,5,6,7],[1,0,4,5],[2,3,7,6],[0,3,7,4],[1,2,6,5]]
    (x,y,z) = cubic_info.shape
    edge_x=[-1, 1, 0, 0, 0, 0];
    edge_y=[0, 0, -1, 1, 0, 0];
    edge_z=[0, 0, 0, 0, -1, 1];
    
    
    counter = np.copy(cubic_info);
    index = 0;
    for ix in range(x):
        for iy in range(y):
            for iz in range(z):
                if(cubic_info[ix][iy][iz] <= 0):
                    continue
                
                # record index for adding link
                counter[ix][iy][iz] = index
                
                # update point
                for pt in t_points:
                    verts.append(link_fulllength * Vector((ix, iy, iz)) + pt)
                
                
                # draw individual cube
                for i in range(6):
                    if(not is_taken(cubic_info, ix + edge_x[i], iy + edge_y[i], iz + edge_z[i])):
                        faces.append([index * 8 + t0 for t0 in t_faceindex[i]])
                        
                # draw link
                for i in range(0, 6, 2):
                    if(is_taken(cubic_info, ix + edge_x[i], iy + edge_y[i], iz + edge_z[i])):
                        index2 = counter[ix + edge_x[i]][iy + edge_y[i]][iz + edge_z[i]]
                        print(index2)
                        face1 = t_faceindex[i]
                        face2 = t_faceindex_inverse[i+1]
                        for t1 in range(4):
                            t2 = (t1 + 1) % 4
                            faces.append([index*8+face1[t1], index*8+face1[t2], index2*8+face2[t2], index2*8+face2[t1]])
                
                # update index
                index = index + 1
                
    print(verts)
    print(faces)
    ## final input
    
    mesh = bpy.data.meshes.new(name="New Cubic Mesh")
    mesh.from_pydata(verts, edges, faces)
    translate(mesh, offsetX)

    
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)
    
    
    return offsetX + link_fulllength * (x + 1)


class CubeImport(Operator, AddObjectHelper, ImportHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.import_cube_file"
    bl_label = "Import Cube Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    # ImportHelper mixin class uses this
    filename_ext = ".cube"

    filter_glob: StringProperty(
        default="*.cube",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    extend_percent: FloatProperty(
        name="extend percent",
        default=0.1,
        description="extend the cube edge according to the percents",
        soft_max=1.0,
        soft_min=0.0,
    )
    

    def execute(self, context):
        print(self.extend_percent)
        cubics_info = read_cube_data(context, self.filepath)
        offsetX = 0
        for cubic in cubics_info:
            offsetX = draw_cube(self, context, cubic, offsetX)
        return {'FINISHED'}


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://github.com/Birdy-C/Puzzle-with-3D-Printer/tree/main/CubeConverter"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(CubeImport)
    bpy.utils.register_manual_map(add_object_manual_map)


def unregister():
    bpy.utils.unregister_class(CubeImport)
    bpy.utils.unregister_manual_map(add_object_manual_map)



if __name__ == "__main__":
    register()
    # test call
    bpy.ops.mesh.import_cube_file('INVOKE_DEFAULT')

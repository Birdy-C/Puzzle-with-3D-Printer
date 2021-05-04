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

def read_cube_data(context, filepath):
    print("running read_some_data...")
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    s1 = data.split('\n');
    s2 = [t0.split('\t') for t0 in s1]
    s3 = [[t1.split(',') for t1 in t0] for t0 in s2]
    cubic_array = np.array(s3).astype(np.int)
    print(cubic_array.shape)
    print(cubic_array)
    return cubic_array

def is_taken(cubic_info, ix, iy, iz):
    (x,y,z) = cubic_info.shape
    if(ix < 0 or iy < 0 or iz < 0):
        return False
    if(ix >= x or iy >= y or iz >= z):
        return False;
    
    return cubic_info(ix, iy, iz) > 0
    
def draw_cube(self, context, cubic_info):

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
        
    t_faceindex = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
    (x,y,z) = cubic_info.shape
    neighbor_link=[-1, -z, -z * y];
    counter = np.copy(cubic_info);
    index = 0;
    for ix in range(x):
        for iy in range(y):
            for iz in range(z):
                if(cubic_info[ix][iy][iz] <= 0):
                    continue
                counter[ix][iy][iz] = index
                for pt in t_points:
                    verts.append(link_fulllength * Vector((ix, iy, iz)) + pt)
                    
                for t_index in t_faceindex:
                    faces.append([index * 8 + t0 for t0 in t_index])
                index = index + 1
                
    print(verts)
    print(faces)
    ## final input
    
    mesh = bpy.data.meshes.new(name="New Cubic Mesh")
    mesh.from_pydata(verts, edges, faces)
    
    # useful for development when the mesh may be invalid.
    mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


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
        default=0.15,
        description="extend the cube edge according to the percents",
        soft_max=1.0,
        soft_min=0.0,
    )
    

    def execute(self, context):
        print(self.extend_percent)
        cubic_info = read_cube_data(context, self.filepath)
        draw_cube(self, context, cubic_info)
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

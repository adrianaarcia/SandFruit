bl_info = {
    "name": "Alien Fruit",
    "authors": "Adriana Arcia",
    "version": (1, 0),
    "blender": (2, 90, 1),
    "location": "View 3d > Tool",
    "warning" : "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
import mathutils
from mathutils import Vector
import random

class MESH_OT_Spikes(bpy.types.Operator):
    bl_label = "Add Spikes"
    bl_idname = "mesh.spikes"
    bl_options = {'REGISTER', 'UNDO'}
    
    radius: bpy.props.FloatProperty(
            name="radius",
            description="radius of base of the spike",
            default = 0.03,
            min=0
            )
    
    length: bpy.props.FloatProperty(
            name="length",
            description="length of the spike",
            default= 1,
            min=0)
            
    
    def execute(self, context):
        fruit = bpy.context.active_object
        
        #create spike
        #bpy.ops.outliner.collection_new(nested=True)
        bpy.ops.mesh.primitive_cone_add(radius1=self.radius, depth=self.length, enter_editmode=False, align='WORLD', 
        location=(0, 0, 0), rotation = (-1.5708,0.0,0.0), scale=(1, 1, 1))
        spike = bpy.context.active_object
        spike.name = "Spike"
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.rotate(value=1.59324, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.translate(value=(0, 0, self.length*0.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.shade_smooth()

        #apply to fruit
        fruit.modifiers.new("part", type='PARTICLE_SYSTEM')
        part = fruit.particle_systems[0]

        settings = part.settings
        settings.type='HAIR'
        settings.use_advanced_hair=True
        settings.emit_from = 'VERT'
        settings.render_type = 'OBJECT'
        settings.instance_object = bpy.data.objects[spike.name]
        settings.use_rotations = True
        settings.rotation_mode = 'NOR'
        


#Register     
classes = [MESH_OT_Spikes]        
        
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    
if __name__ == "__main__":
    register()
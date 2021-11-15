import bpy


class FRUIT_TEXTURE_PT_main_panel(bpy.types.Panel):
    bl_label = "Add Fruit Texture Panel"
    bl_idname = "Fruit_Texture_PT_main_panel"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fruit Texture'

    def draw(self, context):
        layout = self.layout

        layout.operator("fruit_texture.addone_operator")
        row = layout.row()
        layout.operator("fruit_texture.addtwo_operator")
        
        
class FRUIT_TEXTURE_OT_add_one(bpy.types.Operator):
    bl_label = "Add Bump Texture 1"
    bl_idname = "fruit_texture.addone_operator"
    
    col = bpy.props.FloatVectorProperty(name= "Color", subtype= 'COLOR_GAMMA', size=4, default= (0.892,0.701,0.162,1), min = 0, max = 1)
    
    def execute(self, context):
        c = self.col
        
        material_bumpOne = bpy.data.materials.new(name= "Bump One")
        material_bumpOne.use_nodes = True
        
        bpy.context.object.active_material = material_bumpOne
        
        principled_node = material_bumpOne.node_tree.nodes.get('Principled BSDF')
        
        principled_node.inputs[7].default_value = 0.367
        
        rgb_node = material_bumpOne.node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.location = (-250, 0)
        rgb_node.outputs[0].default_value = c
        
        link = material_bumpOne.node_tree.links.new
        
        material_output = material_bumpOne.node_tree.nodes.get('Material Output')
        material_output.location = (400,0)
        
        mus_node = material_bumpOne.node_tree.nodes.new('ShaderNodeTexMusgrave')
        mus_node.location = (-600,0)
        mus_node.musgrave_type = 'MULTIFRACTAL'
        mus_node.inputs[2].default_value = 62
        mus_node.inputs[3].default_value = 0.1
        mus_node.inputs[4].default_value = 25.2
        mus_node.inputs[5].default_value = 5.6
        
        disp_node = material_bumpOne.node_tree.nodes.new('ShaderNodeDisplacement')
        disp_node.location = (-400,0)
        disp_node.inputs[2].default_value = 0.01
        link(rgb_node.outputs[0], principled_node.inputs[0])
        link(mus_node.outputs[0], disp_node.inputs[0])
        link(disp_node.outputs[0], material_output.inputs[2])
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    
class FRUIT_TEXTURE_OT_add_two(bpy.types.Operator):
    bl_label = "Add Bump Texture 2"
    bl_idname = "fruit_texture.addtwo_operator"
    
    col = bpy.props.FloatVectorProperty(name= "Color", subtype= 'COLOR_GAMMA', size=4, default= (0.452,0,0.038,1), min = 0, max = 1)
    
    def execute(self, context):
        
        material_bumpTwo = bpy.data.materials.new(name= "Bump Two")
        material_bumpTwo.use_nodes = True
        
        bpy.context.object.active_material = material_bumpTwo
        
        principled_node = material_bumpTwo.node_tree.nodes.get('Principled BSDF')
        
        rgb_node = material_bumpTwo.node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.location = (-250, 0)
        rgb_node.outputs[0].default_value = self.col
        
        link = material_bumpTwo.node_tree.links.new
        
        link(rgb_node.outputs[0], principled_node.inputs[0])
        
        tc_node = material_bumpTwo.node_tree.nodes.new("ShaderNodeTexCoord")
        
        map_node = material_bumpTwo.node_tree.nodes.new("ShaderNodeMapping")
        noise_node = material_bumpTwo.node_tree.nodes.new("ShaderNodeTexNoise")
        bump_node = material_bumpTwo.node_tree.nodes.new("ShaderNodeBump")
        link(tc_node.outputs[0], map_node.inputs[0])
        link(map_node.outputs[0], noise_node.inputs[0])
        link(noise_node.outputs[1], bump_node.inputs[2])
        link(bump_node.outputs[0], principled_node.inputs[19])
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

classes = [FRUIT_TEXTURE_PT_main_panel, FRUIT_TEXTURE_OT_add_one, FRUIT_TEXTURE_OT_add_two]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

bl_info = {
    "name": "Sandstorm",
    "authors": "Adriana Arcia",
    "version": (1, 0),
    "blender": (2, 90, 1),
    "location": "View 3d > Tool",
    "warning" : "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
import bmesh
import mathutils
import math
from mathutils import Vector
import random

class MESH_OT_Terrain(bpy.types.Operator):
    bl_label = "Add terrain"
    bl_idname = "mesh.terrain"
    
    x_scale: bpy.props.FloatProperty(
            name="x_scale",
            description="x dimension",
            default = 30,
            min=0
            )
    
    y_scale: bpy.props.FloatProperty(
            name="y_scale",
            description="y dimension",
            default= 100,
            min=0)
            
    z_scale: bpy.props.FloatProperty(
            name="z_scale",
            description="width",
            default= 1,
            min=0)
            
    strength: bpy.props.FloatProperty(
            name="strength",
            description="amount of turbulence",
            default= 9,
            min=0)
    
    def addDispMod(self, name, obj, strength, tex):
        mod = obj.modifiers.new(name, 'DISPLACE')
        bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
        mod.texture = tex
        mod.strength = strength
        
        return mod
    
    def execute(self, context):
        '''Add plane (floor) with a collision modifier'''
        #add plane
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=True, align='WORLD', location=(0, 0, 0))
        floor = bpy.context.active_object
        bpy.ops.transform.resize(value=(self.x_scale, self.y_scale, self.z_scale), mirror = True)
        #subdivide
        n_cuts = math.ceil(math.log2(self.x_scale*self.y_scale))
        bpy.ops.mesh.subdivide(number_cuts = n_cuts)
        
        #add a collision modifier
        coll_mod = floor.modifiers.new("collision", 'COLLISION')
        coll = floor.collision
        coll.stickiness = 5.5
        coll.damping_factor = 0.6
        coll.damping_random = 0.29
        coll.friction_factor = 0.4
        coll.friction_random = 0.36
        
        bpy.ops.object.mode_set(mode="OBJECT"
        )
        tex = bpy.data.textures.new("noise", type = 'CLOUDS')
        tex.noise_scale = 4
        strength = self.strength
        disp_mod = self.addDispMod("displacement", floor, strength, tex)
        
        bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
        return {'FINISHED'}
    
class MESH_OT_Sandstorm(bpy.types.Operator):
    bl_label = "Add Sandstorm"
    bl_idname = "mesh.sandstorm"
    bl_options = {'REGISTER', 'UNDO'}
    
    x_scale: bpy.props.FloatProperty(
            name="x_scale",
            description="x dimension",
            default = 2,
            min=0
            )
    
    y_scale: bpy.props.FloatProperty(
            name="y_scale",
            description="y dimension",
            default= 2,
            min=0)
            
    z_scale: bpy.props.FloatProperty(
            name="z_scale",
            description="width",
            default= 8,
            min=0)
    x_rot: bpy.props.FloatProperty(
            name="x_rot",
            description="x rotation",
            default = 1.5708,
            min=0
            )
    y_rot: bpy.props.FloatProperty(
            name="y_rot",
            description="y rotation",
            default = 0,
            min=0
            )
    z_rot: bpy.props.FloatProperty(
            name="z_rot",
            description="z rotation",
            default = 1.5708,
            min=0
            )
    rot_speed: bpy.props.FloatProperty(
            name="z_rot",
            description="z rotation",
            default = 1600,
            min=0
            )
    y_disp: bpy.props.FloatProperty(
            name="displacement",
            description="displacement along y",
            default = 50,
            min=0
            )
    
    def addDispMod(self, name, obj, strength, tex):
        mod = obj.modifiers.new(name, 'DISPLACE')
        bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)
        mod.texture = tex
        mod.strength = strength
        
        return mod
    
    def animateRotation(self, empty, rot, ind):
        empty.rotation_mode='XYZ'
            
        empty.rotation_euler = (0,0,0)
        empty.keyframe_insert('rotation_euler',index=ind,frame=1)    
               
        empty.rotation_euler = rot
        empty.keyframe_insert('rotation_euler',index=ind,frame=250)
        
        fcurves = empty.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
       
    def animateTranslation(self, empty, disp):
        empty.keyframe_insert('location', frame=1)
        empty.location = disp
        empty.keyframe_insert('location',frame=250)
        fcurves = empty.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
                    
    def execute(self, context):
        
        n_divisions = math.ceil(self.z_scale*1.25)
        
        '''get floor'''
        floor = context.active_object
        if floor is None:
            #Add flat terrain with a collision modifier
            bpy.ops.mesh.terrain(strength = 0, x_scale = 5*self.z_scale, y_scale = 2*self.y_disp)
            floor = context.active_object
            bpy.ops.transform.translate(value=(0, 0, -0.125*self.y_scale))
        
        '''Add cylinder (storm) with vertex weight, displacement, and lattice modifiers'''
        #add cylinder
        bpy.ops.mesh.primitive_cylinder_add(enter_editmode=True, align='WORLD', end_fill_type='NOTHING', location=(0, 0, 0.5*self.y_scale), scale=(self.x_scale, self.y_scale, self.z_scale), rotation = (self.x_rot, self.y_rot, self.z_rot))
        cylinder = bpy.context.active_object
        cylinder.name = "Sandstorm"
        #bpy.context.object.display_type = 'WIRE'
        
        #subdivide
        bpy.ops.mesh.select_all(action='DESELECT')
        sel_mode = bpy.context.tool_settings.mesh_select_mode
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        mesh = cylinder.data
        for i in range(1, 32):
            mesh.edges[3*i].select = True
        mesh.edges[1].select = True
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.subdivide(number_cuts=n_divisions)
        
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.shade_smooth()
        
        
        #add vertex group
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        vg = bpy.ops.object.vertex_group_add() ##would cause bug if wrong name
        vg_name = "Group"
        bpy.ops.object.vertex_group_assign()
        bpy.ops.object.mode_set(mode="OBJECT")
        
        #add vertex weight modifier
        vert_mod = cylinder.modifiers.new("vert_wght_prox", 'VERTEX_WEIGHT_PROXIMITY')
        vert_mod.proximity_mode = 'GEOMETRY'
        vert_mod.target = floor
        vert_mod.min_dist = 0.25
        vert_mod.max_dist = 0.75
        vert_mod.vertex_group = vg_name
        
        #add displacement modifier
        tex = bpy.data.textures.new("noise", type = 'CLOUDS')
        tex.noise_scale = 0.9
        strength = 1.5
        name = "displace"
        disp_mod = self.addDispMod(name, cylinder, strength, tex)
        disp_mod.vertex_group = vg_name
        
        
        #add lattice
        scale_factor = 1.25
        lattice_height = scale_factor*self.y_scale
        bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=(0, 0, 0.5*lattice_height))
        lattice = bpy.context.active_object
        bpy.ops.transform.resize(value=(scale_factor*self.z_scale, scale_factor*self.x_scale,lattice_height))
        
        npts_lat = math.ceil(scale_factor*self.y_scale*2)
        lattice.data.points_w = npts_lat
        
        #add lattice modifier
        latt_mod = cylinder.modifiers.new("lattice", 'LATTICE')
        latt_mod.object = lattice
        latt_mod.strength = 1
        #flatten lattice bottom
        sz_each_lat = lattice_height/(npts_lat-1)
        squash_scale = 0.2 #percent to keep of bottommost lat
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        pts = lattice.data.points
        for i in range(0,4): #select bottom verts
            pts[i].select = True
        trans1 = (1-squash_scale)*sz_each_lat
        bpy.ops.transform.translate(value=(0, 0, trans1))
        for i in range(4,8): #select next row of verts
            pts[i].select = True
        trans2 = (1-2*squash_scale)*sz_each_lat
        bpy.ops.transform.translate(value=(0, 0, trans2))
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
        #move down
        cylinder.select_set(True)
        bpy.ops.transform.translate(value=(0, 0, -trans1-trans2))
        
        #resize cylinder
        lattice.select_set(False)
        bpy.context.view_layer.objects.active = cylinder
        bpy.ops.transform.translate(value=(0, 0, 0.1875*self.y_scale))
        bpy.ops.transform.resize(value=(1.25, 1.25, 1.25))
        #bpy.ops.transform.resize(mirror=False,value=(1, 1, 1.15))
        
        #add empty for animation and make cylinder's parent and lattice's parent
        bpy.ops.object.empty_add(type='ARROWS', location=cylinder.location)
        mt = bpy.context.active_object
        cylinder.select_set(True)
        bpy.ops.object.parent_set(type='OBJECT')
        
        #add cylinder particle system
        cylinder.modifiers.new("particles", type='PARTICLE_SYSTEM')
        part = cylinder.particle_systems[0]
        set = part.settings
        
        set.type = 'EMITTER'
        set.count = 10000
        set.object_factor = 1
        set.use_modifier_stack = True
        
        #add fluid dynamics
        fluid_mod = cylinder.modifiers.new("fluid", 'FLUID')
        fluid_mod.fluid_type = 'FLOW'
        
        set = fluid_mod.flow_settings
        set.flow_behavior = 'INFLOW'
        set.flow_source = 'PARTICLES'
        set.particle_system = part
        set.use_initial_velocity = True
        set.temperature = 0.01
        set.particle_size = 0.1
        set.velocity_factor = 0.1
        set.density = 5
        #add bounding box for storm 
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', scale=(2*self.z_scale, 2*self.y_disp, 5*self.y_scale))
        bpy.context.object.display_type = 'WIRE'
        box = context.active_object
        
        box_fm = box.modifiers.new("fluid", 'FLUID')
        box_fm.fluid_type = 'DOMAIN'
        set = box_fm.domain_settings
        set.domain_type = 'GAS'
        set.use_adaptive_domain = True
        set.use_collision_border_bottom = True
        set.time_scale = 0.7
        set.alpha = 0.001
        set.beta = 0.001
        set.vorticity = 0.1
        set.resolution_max = 120
        set.use_noise = False
        bpy.ops.transform.translate(value = (0, 0, 2.5*self.y_scale))
        
        #animate rotation and translation
        rot = (-math.radians(self.rot_speed),0,0)
        self.animateRotation(mt, rot,0)
        disp = (mt.location[0], mt.location[1]+self.y_disp, mt.location[2])
        self.animateTranslation(mt, disp)
        self.animateTranslation(lattice, disp)
        return {'FINISHED'}



#Register     
classes = [MESH_OT_Sandstorm, MESH_OT_Terrain]        
        
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    
if __name__ == "__main__":
    register()
    #bpy.ops.mesh.sandstorm()
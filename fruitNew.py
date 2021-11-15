import bpy
import mathutils
from mathutils import Vector
import random
#this function creates the base pear profile curve
def pearCurve(fruitpoints):
    #then hard code in the base curve for the pear shape
    #vertex 0
    fruitpoints[0].co = Vector((0.0, -1.0964, 0.0))
    fruitpoints[0].handle_left = Vector((-0.3098, -0.8796, 0.0))
    fruitpoints[0].handle_right = Vector((0.5782, -1.5014, 0.0))
    #vertex 1
    fruitpoints[1].co = Vector((0.9462, -0.0319, 0.0))
    fruitpoints[1].handle_left = Vector((0.5293, -0.4809, 0.0))
    fruitpoints[1].handle_right = Vector((1.495, 0.5589, 0.0))
    #vertex 2
    fruitpoints[2].co = Vector((1.0115, 1.0749, 0.0))
    fruitpoints[2].handle_left = Vector((1.1575, 0.8863, 0.0))
    fruitpoints[2].handle_right = Vector((0.8413, 1.2949, 0.0))
    #vertex 3
    fruitpoints[3].co = Vector((0.0, 1.2915, 0.0))
    fruitpoints[3].handle_left = Vector((0.2737, 1.7167, 0.0))
    fruitpoints[3].handle_right = Vector((-0.1327, 1.1394, 0.0))

#this function creates the base apple profile curve
def appleCurve(fruitpoints):
    #hard code in the base curve for the apple shape
    #vertex 0
    fruitpoints[0].co = Vector((0.0, -0.9192, 0.0))
    fruitpoints[0].handle_left = Vector((-0.2431, -0.5807, 0.0))
    fruitpoints[0].handle_right = Vector((0.4913, -1.6032, 0.0))
    #vertex 1
    fruitpoints[1].co = Vector((1.3667, -0.9395, 0.0))
    fruitpoints[1].handle_left = Vector((1.1269, -1.2343, 0.0))
    fruitpoints[1].handle_right = Vector((1.9166, -0.2640, 0.0))
    #vertex 2
    fruitpoints[2].co = Vector((1.0633, 0.9816, 0.0))
    fruitpoints[2].handle_left = Vector((0.9975, 0.6417, 0.0))
    fruitpoints[2].handle_right = Vector((0.9171, 1.4191, 0.0))

    #vertex 3
    fruitpoints[3].co = Vector((0.0, 1.0810, 0.0))
    fruitpoints[3].handle_left = Vector((0.1053, 1.8571, 0.0))
    fruitpoints[3].handle_right = Vector((-0.1084, 0.2827, 0.0))

#this function creates the base lemon profile curve
def lemonCurve(points):
    #hard code in the base curve for the lemon shape
    #vertex 0
    points[0].co = Vector((-0.8877, 0.0, 0.0))
    points[0].handle_left = Vector((-0.9021, -0.1103, 0.0))
    points[0].handle_right = Vector((-0.8830, 0.0338, 0.0))
    
    #vertex 1
    points[1].co = Vector((-0.7702, 0.1239, 0.0))
    points[1].handle_left = Vector((-0.8628, 0.0659, 0.0))
    points[1].handle_right = Vector((-0.6060, 0.2268, 0.0))
    
    #vertex 2
    points[2].co = Vector((0.0049, 0.5895, 0.0))
    points[2].handle_left = Vector((-0.7161, 0.5888, 0.0))
    points[2].handle_right = Vector((0.3185, 0.5897, 0.0))
    
    #vertex 3
    points[3].co = Vector((0.6871, 0.07642, 0.0))
    points[3].handle_left = Vector((0.5324, 0.4092, 0.0))
    points[3].handle_right = Vector((0.6942, 0.06115, 0.0))
    
    #vertex 4
    points[4].co = Vector((0.7573, 0.0, 0.0))
    points[4].handle_left = Vector((0.7790, 0.0833, 0.0))
    points[4].handle_right = Vector((0.7357, -0.0596, 0.0))

#this function jumbles the vectors a bit to add some variation to the shapes
def jumbleVec(vector, jit):
    randoVec = mathutils.noise.random_vector()
    #print("RandoVec = " + randoVec)
    if vector[0] != 0.0:
        vector[0] += randoVec[0] * jit
    if vector[1] != 0.0:
        vector[1] += randoVec[1] * jit
 
 #this function takes the list of fruitpoints and and ups the scale dimensions   
def jumbleScale(fruitpoints, jit):
    randoVec = mathutils.noise.random_vector()
    #print("RandoVec = " + randoVec)
    for point in fruitpoints:
        #co
        point.co[0] *= (1 + jit * randoVec[0])
        point.co[1] *= (1 + jit * randoVec[1])
        #handle_left
        point.handle_left[0] *= (1 + jit * randoVec[0])
        point.handle_left[1] *= (1 + jit * randoVec[1])
        #handle_right
        point.handle_right[0] *= (1 + jit * randoVec[0])
        point.handle_right[1] *= (1 + jit * randoVec[1])
        
def wrinkleFruit(fruit, num):
    fruit = bpy.context.active_object
    bpy.ops.object.editmode_toggle()
    while(num > 0):
        bpy.ops.mesh.select_random(percent=random.randint(20,40),seed=random.randint(0,250))
        bpy.ops.transform.resize(value=(random.uniform(0.8,1), random.uniform(0.8,1), random.uniform(0.8,1)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='SMOOTH', proportional_size=random.uniform(0.25, 0.6), use_proportional_connected=False, use_proportional_projected=False)
        num -= 1
    bpy.ops.object.editmode_toggle()

#create curve
bpy.ops.curve.primitive_bezier_curve_add()

#make curve active object
curve = bpy.context.active_object
curve.name = 'Fruit'

fruitpoints = curve.data.splines[0].bezier_points
#make the curve into pear shape

#start by adding 2 points to the bezier curve
fruitpoints.add(2)
#curve.data.splines[0].bezier_points[2].co = Vector((1.0, 1.0, 0.0))

#change the handle types of the new points to aligned
fruitpoints[2].handle_left_type = 'ALIGNED'
fruitpoints[2].handle_right_type = 'ALIGNED'
#curve.data.splines[0].bezier_points[3].co = Vector((-1.0, 1.0, 0.0))
fruitpoints[3].handle_left_type = 'ALIGNED'
fruitpoints[3].handle_right_type = 'ALIGNED'

choice = random.randint(0, 2)
print(choice)
if choice == 0:
    pearCurve(fruitpoints)
    curve.name = 'Pear'
elif choice == 1:
    fruitpoints.add(1)
    fruitpoints[4].handle_left_type = 'ALIGNED'
    fruitpoints[4].handle_right_type = 'ALIGNED'
    lemonCurve(fruitpoints)
    curve.name = 'Lemon'
else:
    appleCurve(fruitpoints)
    curve.name= 'Apple'

# jitter and rotate curve (if apple)
if choice == 2:
    jitVec = 0.008;
    for point in fruitpoints:
        jumbleVec(point.co, jitVec)
        jumbleVec(point.handle_left, jitVec/2)
        jumbleVec(point.handle_right, jitVec/2)
        
    #jitScale = 0.18
    #jumbleScale(fruitpoints, jitScale)
    
    bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    #add the screw modifier to curve on axis
    bpy.ops.object.modifier_add(type='SCREW')
    bpy.context.object.modifiers["Screw"].axis = 'Y'
    
elif choice == 0:
    jitVec = 0.004;
    for point in fruitpoints:
        jumbleVec(point.co, jitVec)
        jumbleVec(point.handle_left, jitVec)
        jumbleVec(point.handle_right, jitVec)
        
    jitScale = 0.18
    jumbleScale(fruitpoints, jitScale)
    
    bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    #add the screw modifier to curve on axis
    bpy.ops.object.modifier_add(type='SCREW')
    bpy.context.object.modifiers["Screw"].axis = 'Y'
    
else:
    jitVec = 0.001;
    for point in fruitpoints:
        jumbleVec(point.co, jitVec)
        jumbleVec(point.handle_left, jitVec/2)
        jumbleVec(point.handle_right, jitVec/2)
        
    jitScale = 0.12
    jumbleScale(fruitpoints, jitScale)
    
    #add screw modifier to lemon
    bpy.ops.object.modifier_add(type='SCREW')
    bpy.context.object.modifiers["Screw"].axis = 'X'

#convert object to mesh
bpy.ops.object.convert(target='MESH')
fruit = bpy.context.active_object

bpy.ops.object.editmode_toggle()

cycles = random.randint(2,4)

while(cycles > 0):
    bpy.ops.mesh.select_random(percent=random.randint(20,40),seed=random.randint(0,250))
    bpy.ops.transform.translate(value=(random.uniform(-0.08,0.08), random.uniform(-0.08,0.08), random.uniform(-0.08,0.08)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='SMOOTH', proportional_size=random.uniform(0.25, 0.6), use_proportional_connected=False, use_proportional_projected=False)
    cycles -= 1
    
bpy.ops.object.editmode_toggle()

wrinkleFruiit(fruit, random.randint(2,4))



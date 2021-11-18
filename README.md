# SandFruit
Procedural modelling of fruit and sandstorm.
Created by Adriana Arcia and Maya Boateng. Last updated December 19, 2020

## Goal & Inspiration
  Our goal for this project was to create a way of procedurally modeling fruits, specifically exotic fruits, as they have a wide range of shapes and textures that we found interesting. We were inspired by papers about using sweeps of a profile along a path to generate shapes as well as papers about particle systems and surface textures. 
  
  To generate the fruit shapes, we used a general form of a profile of a variety of fruits with round shapes, such as apples, pears, and lemos and used rotation to generate a solid surface. The spike texture was created using a particle system, which we were inspired to after our presentation of Reeves’s paper on particle systems. We also included two bump texturing options for the fruits and added more variance to the shape by jittering random vertices using proportional editing in Blender, and animated a scene with the fruit as part of a sandstorm.

## Roles and Responsibilities
  This project was very collaborative, so there was considerable fluidity in roles and responsibilities. Maya worked primarily on the script that generated the pear meshes, the script that jittered random vertices, and the texturing. Adriana mainly worked on the texturing, sandstorm animation, and building of the scene layout, including the terrain.

## Description of how the code works
  To generate the meshes for the fruit shapes, we first begin with a bezier curve with 4 points on it. Then depending on a random factor that determines the type of fruit shape being generated, a function translates the points and positions the handles in such a way that forms a general shape for the fruit type. Then, the points and handles of the curve are sent to a function that jitters them randomly to create some variation in the profile shape. Finally, the points and handles are scaled by the same random factor in the x and y directions to create some variation in fruit size as well. Then, using the “screw” modifier in Blender, the shape is rotated around an axis to create the solid shape and turned into a mesh.  After this, random vertices are selected and jittered by a random amount to create even more variance in shape and irregularities in the mesh. We also use two different textures to give our fruit an even more bumpy effect without having to make the mesh more complex.
  
  To generate a fruit shape, import the fruitNew.py file into blender and run the script until you have found a desired mesh shape. To add a texture to the fruit, you must install the Fruit texture addon and the panel should show up in the sidebar, where you can choose one of two textures and a base color and apply it to the active object. To add spikes, use spikes.py and run bpy.ops.mesh.spikes() as in our midterm project.
  
  The sandstorm portion of our project is run similarly, by running bpy.ops.mesh.sandstorm(). This function also utilizes another function we implemented, bpy.ops.mesh.terrain(). The inputs are the x scale, y scale, z scale, and the strength of the displacement or the turbulence. The terrain function is a very simple implementation of  terrain generation using ‘cloud’ noise in conjunction with a displacement modifier. If the user wants to use their own terrain or use the terrain function, they should run the sandstorm function with the terrain selected. This will make the sandstorm active on that terrain. If there is no object selected, the sandstorm function defaults to a flat plane. The inputs to the sandstorm terrain are the size of the sandstorm’s base (x, y, and z scale), its rotation (x, y, and z rotation) and the total displacement along the y axis. This last parameter is included because the sandstorm can currently only move in a straight line. 
  
  To create the sandstorm we start with a simple cylinder mesh. We use a similar technique as mentioned earlier for the terrain function to create noise on the surface. Then we also add a vertex weight modifier between the storm and the terrain. We also used a lattice modifier to make the cylinder appear flatter on the bottom as it rotates, to create a more realistic sandstorm. The surface of the cylinder is then used as an emitter for a particle system. We also enable physics for fluids on the cylinder. Then a ‘bounding box’ is added, a cube surrounding the central cylinder which functions as a fluid domain.

## Challenges
  Some challenges associated with the general fruit shape are that the profiles are only loosely based on the general profile of the shape, so certain random jitters can make the fruits look irregular and misshapen beyond any normal irregularities that fruits may have. In addition, sometimes the random selection of vertices or the location of the jitter is strange and leads to the fruit looking strange. This was a problem while attempting to implement aging of the fruit. Subdividing the vertices every couple of iterations may help with these issues.
  
  One challenge with the sandstorm was getting the cylinder not to be too noticeable. This still isn't perfect, and you can see in our animation that it is still fairly darker and distinguishable from the overall sandstorm. It was difficult to find a balance between this aesthetic caveat and having a sandstorm that is full rather than sparse.

## Future ideas/expansion
  In the future, it may be possible to refine the functions that generate the profile shapes so that there are not as many unnatural looking ridges and bumps, and possibly use a more mathematical function to generate the profiles instead of hard coding them in, in addition to writing functions for more types of fruit families. There is also the possibility of using the bevel function rather than the “screw” modifier to generate the shapes, by having the profile beveled around a circle or any other closed shape. This would allow us to define sections within the fruit shape to give a taper to the radius at certain points around the 
edge of the fruit, like that of a pumpkin. We could also add in a function to generate stem shapes of the fruits by extruding a profile along an arc or path with a taper defined for the size of the profile at a given point along the path. Although we attempted this, we would like to continue to try to animate and model the aging of fruits in some way, even if it is an imaginary framework. While trying to select random vertices and scale them down iteratively, we encountered jagged edges and little change beyond what we were getting from the vertex jitter.

It would also be ideal if the sandstorm could move more flexibly instead of moving in a straight line. It also does not work as smoothly on non-flat terrain, so there is room for improvement in terms of being more dynamic. As mentioned earlier, there could be some improvement made to help the cylinder particle system less noticeable. We also did not get a chance to improve much on our spikes, which could still be perfected with more randomness and perhaps adding curvature.

## Results
The `results` folder contains screenshots of some possible output.

## Sources
Reeves, W. T. (1983). Particle Systems—a Technique for Modeling a Class of Fuzzy Objects. ACM Transactions on Graphics, 2(2), 91-108. doi:10.1145/357318.357320

John M. Snyder California Institute of Technology et al. 1992. Generative modeling: a symbolic system for geometric modeling. (July 1992). Retrieved October 19, 2020 from https://dl.acm.org/doi/10.1145/133994.134094 

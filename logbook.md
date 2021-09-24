# Polar Zonohedra Logbook

## 2021-09-21 Initial Setup

Today I set up the repo and started generating vertices/indices. Most of the
way there, but still have faces and mesh generation to go.

Next Steps:

* Debug vertices, some values sem to be missing.
* Determine how to generate faces
* Determine how to generate a mesh with PyMesh. or perhaps OpenMesh?

## 2021-09-23 Faces

Today I added a function to compute the face indices.

Next Steps:

* Debug vertices
* Determine how to generate the mesh

## 2021-09-24 Generated a Mesh

Today I fixed the vertices and generated an OBJ mesh.

For now, that's all I want to do for this project, if I want to generate
a glTF, I'll probably open the mesh in Blender to customize it.
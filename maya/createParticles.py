# createParticles.py

import maya.cmds as cmds

def create():
    cmds.polyCylinder(radius=1,height=0.04,subdivisionsX=6)
    selection = cmds.ls(selection=True)
    cmds.polyBevel3(selection,fraction=0.5,offsetAsFraction=1,autoFit=1,depth=1,mitering=0,miterAlong=0,chamfer=1,segments=1,worldSpace=1,smoothingAngle=30,subdivideNgons=1,mergeVertices=1,mergeVertexTolerance=0.0001,miteringAngle=180,angleTolerance=180)

if __name__ == "__main__":
    create()
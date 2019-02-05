# randomInstances.py

import maya.cmds 
import random

result = cmds.ls(orderedSelection=True)

instanceName = result[0]
instanceGroupName = cmds.group(empty=True,name=instanceName+ '_instance_grp#')

for i in range(0,50):
    instanceResult= cmds.instance(instanceName,name=instanceName+'_instance'+str(i))
    cmds.parent(instanceResult,instanceGroupName)
    
    x=random.uniform(-8,8)
    y=random.uniform(0,11)
    z=random.uniform(-8,8) 
    xr=random.uniform(0,360)
    yr=random.uniform(0,360)
    zr=random.uniform(0,360)
    scalingFactor = random.uniform(0.5,1.3)
    
    cmds.move(x,y,z,instanceResult)
    cmds.rotate(xr,yr,zr,instanceResult)
    cmds.scale(scalingFactor,scalingFactor,scalingFactor,instanceResult)

cmds.hide(instanceName)
cmds.xform(instanceName,centerPivots=True)

# Place sphere in center
cmds.polySphere(radius=1,subdivisionsX=20,subdivisionsY=20)
cmds.move(5.5,y=True)
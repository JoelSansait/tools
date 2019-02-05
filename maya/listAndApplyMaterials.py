import maya.cmds as cmds
import random

# Create a list of MDLs that can be found in Hypershade
def create_mdl_list():
	mdllist = []
	for shaders in cmds.listNodeTypes('shader'):
		if 'mdl' in shaders: 
			if shaders in mdllist:
				mdllist.append(shaders + '_copy')
			mdllist.append(shaders)

	return mdllist

# Randomly place spheres everywhere and apply all the materials to them
def sphere_placement(mdllist):
	cmds.polySphere(sx = 20, sy = 30, r = 0.5, name='sphere')
	result = cmds.ls(orderedSelection=True)
	instanceName = result[0]
	instanceGroupName = cmds.group(empty=True,name=instanceName+ '_instance_grp#')

	for i, mdl in enumerate(mdllist):
		instanceResult= cmds.instance(instanceName,name=instanceName+'_instance'+str(i))
		cmds.parent(instanceResult,instanceGroupName)

		x=random.uniform(-10,10)
		y=random.uniform(0,17)
		z=random.uniform(-10,10) 
		xr=random.uniform(0,360)
		yr=random.uniform(0,360)
		zr=random.uniform(0,360)
		scalingFactor = random.uniform(0.8,1.8)

		cmds.move(x,y,z,instanceResult)
		cmds.rotate(xr,yr,zr,instanceResult)
		cmds.scale(scalingFactor,scalingFactor,scalingFactor,instanceResult)

		mat = cmds.shadingNode(mdl, name='test_%s' % mdl, asShader=True)
		matSG = cmds.sets(name='%sSG' % mat, empty=True, renderable=True, noSurfaceShader=True)
		cmds.connectAttr('%s.outColor' % mat, '%s.surfaceShader' % matSG)
		cmds.sets(instanceResult, e=True, forceElement=matSG)


listofmdl = create_mdl_list()
sphere_placement(listofmdl)
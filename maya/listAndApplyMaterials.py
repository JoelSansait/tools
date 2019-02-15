import maya.cmds as cmds
import random
import datetime


# Create a list of MDLs that can be found in Hypershade
def create_mdl_list():
	mdllist = []
	# for shaders in cmds.listNodeTypes('shader'):
	# 	if 'mdl' in shaders: 
	# 		if shaders in mdllist: # Check for dupe
	# 			mdllist.append(shaders + '_copy')
	# 		else:
	# 			mdllist.append(shaders)
	for shaders in cmds.listNodeTypes('shader'):
		if 'mdl' in shaders and shaders not in mdllist:
			mdllist.append(shaders)
	return mdllist


# Randomly place spheres everywhere and apply all the materials to them
def sphere_placement(mdllist):
	cmds.polySphere(sx = 12, sy = 12, r = 50, name='sphere')
	result = cmds.ls(orderedSelection=True)
	instanceName = result[0]
	instanceGroupName = cmds.group(empty=True,name=instanceName+ '_instance_grp#')

	for i, mdl in enumerate(mdllist):
		instanceResult= cmds.instance(instanceName,name=instanceName+'_instance'+str(i))
		cmds.parent(instanceResult,instanceGroupName)

		x=random.uniform(-600,600)
		y=random.uniform(-400,400)
		z=random.uniform(-700,700) 
		xr=random.uniform(0,360)
		yr=random.uniform(0,360)
		zr=random.uniform(0,360)
		scalingFactor = random.uniform(0.8,1.8)

		cmds.move(x,y,z,instanceResult)
		cmds.rotate(xr,yr,zr,instanceResult)
		cmds.scale(scalingFactor,scalingFactor,0.7*scalingFactor,instanceResult)

		mat = cmds.shadingNode(mdl, name='test_%s' % mdl, asShader=True)
		matSG = cmds.sets(name='%sSG' % mat, empty=True, renderable=True, noSurfaceShader=True)
		cmds.connectAttr('%s.outColor' % mat, '%s.surfaceShader' % matSG)
		cmds.sets(instanceResult, e=True, forceElement=matSG)


def sphere_placement_nogroups(mdllist):
	scalingFactor = random.uniform(0.8,1.8)
	# Create initial sphere 
	cmds.polySphere(sx = 12, sy = 12, r = 50, name='sphere_origin')

	# Create randomly placed sphere and apply a MDL to it
	for i, mdl in enumerate(mdllist):
		# Scaling parameters
		x=random.uniform(-600,600)
		y=random.uniform(-400,400)
		z=random.uniform(-700,700) 
		xr=random.uniform(0,360)
		yr=random.uniform(0,360)
		zr=random.uniform(0,360)

		cmds.polySphere(sx = 12, sy = 12, r = 50, name='sphere_%s' % i)
		result = cmds.ls(orderedSelection=True)
		instanceName = result[0]

		cmds.move(x,y,z,instanceName)
		cmds.rotate(xr,yr,zr,instanceName)
		cmds.scale(scalingFactor,scalingFactor,0.7*scalingFactor,instanceName)

		mat = cmds.shadingNode(mdl, name='test_%s' % mdl, asShader=True)
		matSG = cmds.sets(name='%sSG' % mat, empty=True, renderable=True, noSurfaceShader=True)
		cmds.connectAttr('%s.outColor' % mat, '%s.surfaceShader' % matSG)
		cmds.sets(instanceName, e=True, forceElement=matSG)


# Exports current scene to a folder. Deletes folder if it already exists
def export_folder():
	thetime = datetime.datetime.now()
	sceneURL = '/Users/joel/test/%s/mdl_workflow_test.usd' % thetime.strftime("%Y%m%d%H%M")
	#sceneURL= '/Users/joel/test/%s/%s.usd' % (mdl_from_list, mdl_from_list)
	cmds.optionVar( sv=('server_url_var', 'ws://ov-prod:3009') )
	cmds.optionVar( sv=('omniverse_user_name_var', 'joel') )
	cmds.optionVar( sv=('omniverse_user_password_var', 'joel') )
	cmds.optionVar( sv=('omniverse_update_interval_ms', '100') )
	cmds.optionVar( sv=('all_url_var', '') )
	#connect
	cmds.OmniConfigCmd( )
	#delete if exists
	cmds.OmniDeleteCmd( file=sceneURL )
	#save scene
	cmds.OmniExportCmd( file=sceneURL )
	cmds.OmniListCmd( )


if __name__ == "__main__":

	listofmdl = create_mdl_list()
	#print(listofmdl)
	sphere_placement_nogroups(listofmdl)
	#export_folder()


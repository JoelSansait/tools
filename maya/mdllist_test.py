import maya.cmds as cmds

# Create a list of MDLs that can be found in Hypershade

mdllist = []
for shaders in cmds.listNodeTypes('shader'):
	if 'mdl' in shaders: 
		if shaders in mdllist:
			mdllist.append(shaders + '_copy')
		else:
			mdllist.append(shaders)

print(mdllist)
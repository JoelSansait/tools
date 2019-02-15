import maya.cmds as cmds

"""
Modifcation of listAndApplyMaterials.py

Creates 1 mesh for 1 folder, and export.
"""

# Create list of existing MDLs
def create_mdl_list():
	mdllist = []
	for shaders in cmds.listNodeTypes('shader'):
		if 'mdl' in shaders: 
			if shaders in mdllist: # Check for dupe
				mdllist.append(shaders + '_copy')
			else:
				mdllist.append(shaders)
	return mdllist

# Create mesh and apply mdl to mesh. Should be done in a for loop
def create_and_apply_materials(mdl_from_list):
	cmds.polySphere(sx = 20, sy = 30, r = 0.5, name='sphere')
	mesh = cmds.ls(orderedSelection=True)

	mat = cmds.shadingNode(mdl_from_list, name='test_%s' % mdl_from_list, asShader=True)
	matSG = cmds.sets(name='%sSG' % mat, empty=True, renderable=True, noSurfaceShader=True)
	cmds.connectAttr('%s.outColor' % mat, '%s.surfaceShader' % matSG)
	cmds.sets(mesh, e=True, forceElement=matSG)

# Exports current scene to a folder. Should be done in a for loop.
def export_folder(mdl_from_list):
	sceneURL= '/Users/joel/test/%s/%s.usd' % (mdl_from_list, mdl_from_list)
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


listofmdl = create_mdl_list()

for material in listofmdl:
	# Create mesh+material
	# Export
	# Clear scene
	# Do it again
	create_and_apply_materials(material)
	export_folder(material)
	cmds.file( f=True, new=True )

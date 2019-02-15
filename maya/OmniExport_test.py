import maya.cmds as cmds


#load ma scene
#sceneFileName='C:\\Users\\qajoel\\Documents\\maya\\projects\\default\\scenes\\material_test.ma'
sceneURL= '/Users/joel/test/test.usd'
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
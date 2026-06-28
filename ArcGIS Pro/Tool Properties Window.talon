os: windows
and app.name: ArcGIS Pro
and win.title: /^Tool Properties:.*/
os: windows
and app.exe: /^arcgispro\.exe$/i
and app.title: /^Tool Properties:.*/
-
column select {user.arc_tool_properties_parameter_column}: user.arc_tool_properties_select_column(arc_tool_properties_parameter_column)
row select <user.text>: 
	user.arc_tool_properties_select_row(text)
hello: print("asparagus")
os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-

run tool$: user.arc_run_tool()
run tool {user.arc_geoprocessing_tool}$: user.arc_run_tool("{arc_geoprocessing_tool}")

# GEOPROCESSING PANEL
toolbox {user.arc_dynamic_toolbox}: user.arc_nav_toolbox(arc_dynamic_toolbox)
geoprocessing {user.arc_geoprocessing_tool}: user.arc_run_tool(arc_geoprocessing_tool)
geoprocessing search: user.arc_run_tool()

# PARAMETERS
parameter [select] {user.arc_gp_dynamic_parameter}: user.arc_select_parameter(arc_gp_dynamic_parameter)
parameter browse {user.arc_gp_dynamic_parameter}: user.arc_select_parameter(arc_gp_dynamic_parameter,'browse')
parameter expand {user.arc_gp_dynamic_parameter}: user.arc_select_parameter(arc_gp_dynamic_parameter,'expand')
parameter toggle {user.arc_gp_dynamic_parameter}: user.arc_select_parameter(arc_gp_dynamic_parameter,'toggle')


# REPLACED
#^parameter {user.arc_parameter}$: user.arc_tab_to_parameter(arc_parameter)
os: windows
and app.name: ArcGIS Pro
and win.title: ArcGIS Pro
os: windows
and app.exe: /^arcgispro\.exe$/i
and win.title: ArcGIS Pro
-
select <user.ordinals> project: user.arc_act_on_project_by_id(ordinals,'select')
open <user.ordinals> project: user.arc_act_on_project_by_id(ordinals,'open')

project select [<user.ordinals>] {user.arc_dynamic_project}: user.arc_act_on_project(arc_dynamic_project, "select", ordinals or 1)
project open [<user.ordinals>] {user.arc_dynamic_project}: user.arc_act_on_project(arc_dynamic_project, "open", ordinals or 1)
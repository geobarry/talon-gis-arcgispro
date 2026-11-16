# ArcGIS Pro Calculate Field dialog does not have a title so we will just have to settle for restricting this to windows without any title
os: windows
and app.name: ArcGIS Pro
and win.title: /^$/i
os: windows
and app.exe: /^arcgispro\.exe$/i
and win.title: /^$/i
-
[calculate field] Input Table: user.arc_calc_field_select("Input Table")
[calculate field] Field Name: user.arc_calc_field_select("Field Name")
[calculate field] Expression Type: user.arc_calc_field_select("Expression Type")
[calculate field] Fields: user.arc_calc_field_select("Fields")
[calculate field] Helpers: user.arc_calc_field_select("Helpers")
[calculate field] Expression: user.arc_calc_field_select("Expression")
[calculate field] Code Block: user.arc_calc_field_select("Code Block")
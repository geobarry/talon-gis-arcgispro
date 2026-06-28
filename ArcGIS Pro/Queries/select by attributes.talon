os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-
{user.arc_field_name} select <user.constructed_text>:
	user.arc_quick_select_by_attributes(arc_field_name,constructed_text)
{user.arc_field_name} assign value <user.constructed_text>:
	user.arc_quick_assign_value(arc_field_name,constructed_text)
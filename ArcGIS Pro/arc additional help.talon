os: windows
#app.exe: arcgispro.exe
mode: command
mode: user.zen
-

arc help {user.arc_command_modules}: user.arc_help_module(arc_command_modules)
arc help {user.arc_menu_heading_name} menu: user.help_list("user.arc_menu_item",false,true,"{arc_menu_heading_name}")
arc help list {user.arc_list}: user.help_list(arc_list,false,true)
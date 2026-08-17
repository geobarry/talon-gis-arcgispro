os: windows
#app.exe: arcgispro.exe
mode: command
mode: user.zen
-
# COMMAND MODULES
arc help$: user.arc_help_module("arc help")
arc help command modules$: user.help_list("user.arc_command_modules",false,true)
arc help menu headings$: user.help_list("user.arc_menu_heading")
arc help lists$: user.help_list("user.arc_list",false,true)
arc help search <user.text>$: user.arc_help_search(text)
help close$: user.close_arc_help_search()


os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-
arc help: user.arc_help_module("arc help")
arc help navigation: user.arc_help_module("navigation")
arc help menu$: user.help_list("user.arc_ribbon_heading")
arc help {user.arc_ribbon_heading} menu: user.help_list("user.arc_ribbon_item",false,true,"{arc_ribbon_heading}")
arc help contents: user.arc_help_module("contents")
arc help symbology: user.arc_help_module("Symbology.symbology")

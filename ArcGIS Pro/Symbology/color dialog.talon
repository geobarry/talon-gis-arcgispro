os: windows
and app.exe: /^arcgispro\.exe$/i
and win.title: /Color Editor/i
-
select red: user.arc_color_dialog_property("red")
select green: user.arc_color_dialog_property("green")
select blue: user.arc_color_dialog_property("blue")
select transparency: user.arc_color_dialog_property("transparency")
select HEX: user.arc_color_dialog_property("HEX.*")

red <number>: user.arc_color_dialog_property("red", number)
green <number>: user.arc_color_dialog_property("green", number)
blue <number>: user.arc_color_dialog_property("blue", number)
transparency <number>: user.arc_color_dialog_property("transparency", number)
HEX {user.color}: user.arc_color_dialog_property("HEX.*", color)
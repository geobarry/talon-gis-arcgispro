os: windows
and app.exe: /^arcgispro\.exe$/i
and win.title: /.*Properties:.*/i
-
dialog {user.arc_button}: user.arc_dialog_button(arc_button,"Invoke")

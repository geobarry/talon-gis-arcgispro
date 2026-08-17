os: windows
and app.exe: /^arcgispro\.exe$/i
and win.title: /(.*Properties:.*|Color Editor)/i
-
dialog {user.arc_button}: user.arc_dialog_button(arc_button,"Invoke")

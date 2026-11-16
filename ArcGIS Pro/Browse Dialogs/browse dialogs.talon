os: windows
and app.name: ArcGIS Pro
and win.title: /^(Join Table|Output Feature Class)$/i
os: windows
and app.exe: /^arcgispro\.exe$/i
and win.title: /^(Join Table|Output Feature Class)$/i
-
folder from clipboard: user.arc_browse_set_folder()
panel content: user.arc_browse_focus_content()
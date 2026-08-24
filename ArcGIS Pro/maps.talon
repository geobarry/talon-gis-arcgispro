os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-

zoom in: user.arc_call_menu_item("Map,Navigate,,Fixed Zoom In")
zoom out: user.arc_call_menu_item("Map,Navigate,,Fixed Zoom Out")


(navigate|nav|center map on) <user.arc_coordinate>: user.arc_nav_coord(arc_coordinate)
(navigate|nav|center map on)$: user.arc_nav_coord()
representative fraction [<number>]: user.arc_scale_text(number or 0)


pan {user.compass_direction}: user.arc_pan(compass_direction,0.25)
pan (far|way) {user.compass_direction}: user.arc_pan(compass_direction,0.9)
pan (tiny|a little bit) {user.compass_direction}: user.arc_pan(compass_direction,0.05)

pan west <number>: user.pan_arcgis_pro_map('west',number)
pan east <number>: user.pan_arcgis_pro_map("east",number)
pan north <number>: user.pan_arcgis_pro_map('north',number)
pan south <number>: user.pan_arcgis_pro_map('south',number)
orient [north]: key(o)
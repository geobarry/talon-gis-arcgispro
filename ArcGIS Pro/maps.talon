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


pan <user.four_directions>: user.drag_window_center(four_directions,25)
pan <number> <user.four_directions>: user.drag_window_center(four_directions,number)
pan (far|way) <user.four_directions>: user.drag_window_center(four_directions,49)
pan (tiny|a little bit) <user.four_directions>: user.drag_window_center(four_directions,5)

orient [north]: key(o)
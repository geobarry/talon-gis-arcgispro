os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-

# PANELS
show panels: key(ctrl:down tab)
choose panel: key(ctrl:up)
panel [select] {user.arc_panel}: user.quick_select_panel(arc_panel)
map [select] [<user.ordinals>] {user.arc_dynamic_map}$: user.arc_select_panel(arc_dynamic_map, ordinals or 1)
layout [select] [<user.ordinals>] {user.arc_dynamic_layout}$: user.arc_select_panel(arc_dynamic_layout, ordinals or 1)
table [select] [<user.ordinals>] {user.arc_dynamic_table}$: user.arc_select_panel(arc_dynamic_table, ordinals or 1)

catalog [select] {user.arc_catalog_group}: user.arc_select_catalog_group(arc_catalog_group)

# TABS (MAPS,LAYOUTS,TABLES)
# A tab is within a group, i.e. [maps,layouts,tables] or [catalog, ...]
(tab|panel|map|layout|table) close: key("ctrl-f4")
(tab|panel|map|layout|table) next: key("ctrl-f6")
(tab|panel|map|layout|table) previous: key("ctrl-shift-f6")

# BUTTONS
{user.arc_button} button: user.arc_tab_to_button(arc_button,true)
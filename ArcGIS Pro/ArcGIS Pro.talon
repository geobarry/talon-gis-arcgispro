os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-

# PANELS
show panels: key(ctrl:down tab)
choose panel: key(ctrl:up)
contents: user.arc_select_contents()
panel [select] {user.arc_dynamic_panel}$: user.arc_select_panel(arc_dynamic_panel,true)
catalog [select] {user.arc_catalog_group}: user.arc_select_catalog_group(arc_catalog_group)

# TABS (MAPS,LAYOUTS,TABLES)
# A tab is within a group, i.e. [maps,layouts,tables] or [catalog, ...]
(tab|panel) close: key("ctrl-f4")
(tab|panel) next: key("ctrl-f6")
(tab|panel) previous: key("ctrl-shift-f6")

# BUTTONS
{user.arc_button} button: user.arc_tab_to_button(arc_button,true)

# CONTENTS PANEL
list by Drawing Order: user.arc_contents_list_by('esri_mapping_DrawingOrderView')
list by Data Source: user.arc_contents_list_by('esri_mapping_DataSourceView')
list by Selection: user.arc_contents_list_by('esri_mapping_SelectionView')
list by Editing: user.arc_contents_list_by('esri_editing_EditingView')
list by Snapping: user.arc_contents_list_by('esri_mapping_SnappingView')
list by Labelling: user.arc_contents_list_by('esri_mapping_LabelingView')
list by Prospective Imagery: user.arc_contents_list_by('esri_mapping_ImageSpaceItemsView')



# CONTENTS PANEL LAYERS
layer select {user.arc_dynamic_layer}: user.arc_select_layer(arc_dynamic_layer,false)
layer copy {user.arc_dynamic_layer}: user.arc_copy_layer(arc_dynamic_layer,false)
layer expand {user.arc_dynamic_layer}: user.arc_expand_collapse_layer(arc_dynamic_layer,"expand")
layer collapse {user.arc_dynamic_layer}: user.arc_expand_collapse_layer(arc_dynamic_layer,"collapse")
layer {user.arc_layer_context_item}: user.arc_context_item(arc_layer_context_item)
layer up: user.arc_drag_list_item("up")
layer down: user.arc_drag_list_item("down")
map properties: user.arc_context_item("Properties")
map projection: user.arc_map_coordinate_system()
^go to map$: user.arc_select_map_in_contents()

# RIBBON
^menu {user.arc_ribbon_heading}$: user.arc_open_ribbon(arc_ribbon_heading)
^{user.arc_ribbon_item}$: user.arc_call_ribbon_item(arc_ribbon_item)
# more verbose version
[open the] {user.arc_ribbon_heading} menu: user.arc_open_ribbon(arc_ribbon_heading)
# inserts text into the textbox just after the label with a given text
insert text: user.arc_insert_text()

# RIBBON SHORTCUTS
zoom in: user.arc_call_ribbon_item("Map,Navigate,,Fixed Zoom In")
zoom out: user.arc_call_ribbon_item("Map,Navigate,,Fixed Zoom Out")

# OVERRIDES
^{user.nav_key} until <user.lazy_target>$:
	user.arc_key_to_element(nav_key,"n={lazy_target}.*")

^{user.nav_key} until <user.ordinals> <user.lazy_target>$:
	user.arc_key_to_element(nav_key,"n={lazy_target}.*",ordinals)


# GENERAL CONVENIENCE
# say this after selecting any command that requires you to then draw a rectangle onto the layout

create [(custom|new)] <user.real_number> by <user.real_number> layout: user.arc_create_custom_layout(real_number_1, real_number_2)
place (on|onto) layout: user.arc_draw_rectangle_on_layout()
expand map to layout: user.arc_expand_map_to_layout()


position ex <user.real_number>: user.arc_set_position("X",real_number)
position why <user.real_number>: user.arc_set_position("Y",real_number)
shape width <user.real_number>: user.arc_set_position("Width",real_number)
shape height <user.real_number>: user.arc_set_position("Height",real_number)





# MAPS
(navigate|nav|center map on) <user.arc_coordinate>: user.arc_nav_coord(arc_coordinate)
(navigate|nav|center map on)$: user.arc_nav_coord()
[click on] representative fraction: user.arc_scale_text()


# WHY ISN'T THE TALON LIST BEING RECOGNIZED???
content map {user.arc_contents_map_context_item}: 
	#user.arc_contents_nav_map_context_item(arc_contents_map_context_item)
	print("command recognized")

# SHARED
select color$: user.arc_color_editor_window()
select color {user.color}: user.arc_select_color(color)
select color transparency <number>: user.arc_select_color_transparency(number)

add data: key(esc:5 alt m a d down enter)

# ESRI shortcuts
toggle ribbon: key("ctrl-f1")
keyboard shortcuts: key("f12")
copy path: key("ctrl-alt-p")
new map: key("ctrl-m")
export: 
	key("ctrl-e")
	user.key_to_elem_by_val("tab","Browse.*","Name")
	key("shift-tab ctrl-a")
command search: key("alt-q")
panel options: key("alt-minus")
close panel: key("shift-esc")
next command: key("tab")
previous command: key("shift-esc")
next (element|item): key("down")
previous (element|item): key("up")
next (map|layout|view): key("ctrl-f6")
previous (map|layout|view): key("ctrl-shift-f6")

# Catalog Pane
go to catalog folders: key("esc:5 alt-v c p alt-f6 pageup f")
go to catalog maps: key("esc:5 alt-v c p alt-f6 pageup m down up")
go to catalog (database|databases): key("esc:5 alt-v c p alt-f6 pageup d")
go to catalog layouts: key("esc:5 alt-v c p alt-f6 pageup l")
go to catalog notebooks: key("esc:5 alt-v c p alt-f6 pageup n")
add folder connection: key("ctrl-shift-c")
add [geo] database connection: key("ctrl-shift-e")
project context menu: key("ctrl-shift-n")
# When folder is selected in catalog pane
new folder: key("ctrl-shift-f")
new [geo] database: key("ctrl-shift-d")
refresh: key("f5")


# Contents Pane
next layer: user.arc_contents_nav_to_layer_item("down")
previous layer: user.arc_contents_nav_to_layer_item("up")
expand: key("right")
collapse: key("left")
expand level: key("ctrl-plus")
collapse level: key("ctrl-minus")
expand all: key("ctrl-shift-plus")
collapse all: key("ctrl-shift-minus")
toggle visibility: key(space)
definition query: user.slow_key_press("enter pageup:3 down:7 tab")
export features: key("alt t v e f")
export table: key("alt t v e t")
layer properties: 
	key(menu)
	user.key_to_elem_by_val("up","Properties")
	key("enter")




# Catalogue Pane
add to current map: key(menu a)

# Map Navigation
pan {user.compass_direction}: user.arc_pan(compass_direction,0.25)
pan (far|way) {user.compass_direction}: user.arc_pan(compass_direction,0.9)
pan (tiny|a little bit) {user.compass_direction}: user.arc_pan(compass_direction,0.05)

pan west <number>: user.pan_arcgis_pro_map('west',number)
pan east <number>: user.pan_arcgis_pro_map("east",number)
pan north <number>: user.pan_arcgis_pro_map('north',number)
pan south <number>: user.pan_arcgis_pro_map('south',number)
orient [north]: key(o)

select by attributes:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(m s b a)
clear selection: key(esc:5 alt m c x)

# DEVELOPMENT
^ribbon copy {user.arc_ribbon_heading} items$: user.arc_get_ribbon_items(arc_ribbon_heading) 

# MENU ITEM SHORTCUTS - do we need these anymore?
# insert menu shortcuts
# new map command already mapped above
new layout: key(alt n n l)
new custom layout: key(alt n n l c tab:4)
(new|add) map frame: key(alt n m g)

# analysis menu shortcuts
new jupyter notebook: user.slow_key_press("alt-a p f down right:3 enter",1.0)

# edit short cuts
save edits:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(e s v)
	
# layout menu shortcuts

# table menu shortcuts
add field:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(t v f n)
zoom [to] selected: key(alt t v r z)
flash (selected|active): key(alt t v r f)
pan [to] (selected|active): key(alt t v r p)

	
# field many shortcuts
save fields:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(f s v)
# share menu shortcuts
export layout:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(s x l)
	sleep(0.5)
	key(down:3)
# map frame menu shortcuts
[set] (text|map|legend|scale bar|north arrow|arrow|line|shape) position: 
	key(esc:5 alt j f s p)
	user.key_to_elem_by_val("tab","TextBox","class_name")
	key(ctrl-a)
flip vertical: key(alt j f r v)
flip horizontal: key(alt j f r v)



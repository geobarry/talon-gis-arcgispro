os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-

# GENERAL CONVENIENCE
# say this after selecting any command that requires you to then draw a rectangle onto the layout

create [(custom|new)] <user.real_number> by <user.real_number> layout: user.arc_create_custom_layout(real_number_1, real_number_2)
map frame insert {user.arc_dynamic_map}: user.arc_insert_map_frame(arc_dynamic_map)
place (on|onto) layout: user.arc_draw_rectangle_on_layout()
map expand to layout: user.arc_expand_map_to_layout()
map expand to <user.real_number> by <user.real_number> layout: user.arc_expand_map_to_layout(real_number_1, real_number_2)

position ex <user.real_number>: user.arc_set_position("X",real_number)
position why <user.real_number>: user.arc_set_position("Y",real_number)
shape width <user.real_number>: user.arc_set_position("Width",real_number)
shape height <user.real_number>: user.arc_set_position("Height",real_number)

show undo list: user.arc_show_undo_list()

# OVERRIDES
^{user.nav_key} until <user.lazy_target>$:
	user.arc_key_to_element(nav_key,"n={lazy_target}.*")

^{user.nav_key} until <user.ordinals> <user.lazy_target>$:
	user.arc_key_to_element(nav_key,"n={lazy_target}.*",ordinals)

insert text: user.arc_insert_text()


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

keyboard shortcuts: key("f12")
copy path: key("ctrl-alt-p")
new map: key("ctrl-m")
export: 
	key("ctrl-e")
	user.key_to_elem_by_val("tab","Browse.*","Name")
	key("shift-tab ctrl-a")
command search: key("alt-q")


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
definition query: user.arc_definition_query()
export features: key("alt t v e f")
export table: key("alt t v e t")





# Catalogue Pane
add to current map: key(menu a)



select by attributes:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(m s b a)
clear selection: key(esc:5 alt m c x)


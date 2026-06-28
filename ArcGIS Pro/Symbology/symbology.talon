os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-
primary symbology [{user.ui_action}] {user.arc_primary_symbology_control}: user.control_primary_symbology(arc_primary_symbology_control,ui_action or "select")

# SYMBOLOGY PANEL
symbology menu: key("alt j a d s")
#primary symbology: user.arc_tab_to_primary_symbology()
primary symbology$: user.arc_select_primary_symbology()
[primary] symbology {user.arc_primary_symbology}$: user.arc_select_primary_symbology(arc_primary_symbology)

properties tab:
	user.arc_symbology_tabs()
	key("right")
gallery tab:
	user.arc_symbology_tabs()
	key("left")

symbol gallery: user.arc_symbol_tab("gallery")

symbol properties: user.arc_symbol_property_tab("Properties")
symbol layers: user.arc_symbol_property_tab("Layers")
symbol structure: user.arc_symbol_property_tab("Structure")

symbol {user.arc_symbol_property_group}: user.arc_symbol_property_group(arc_symbol_property_group)
symbol {user.arc_symbol_control}$: user.arc_symbol_control(arc_symbol_control)

symbol {user.arc_color_symbol_control} {user.color}: user.arc_symbol_assign_color(arc_color_symbol_control,color)

<user.ordinals> symbol: user.arc_nav_nth_symbol(ordinals)
split down:
	user.key_to_elem_by_val("tab","Grid splitter")
	key("down:7")
split up:
	user.key_to_elem_by_val("tab","Grid splitter")
	key("up:7")


button burger: user.key_to_name_and_class("tab","$","Button_Burger")
import symbology: user.arc_import_symbology()

# DEVELOPMENT
^symbology copy {user.arc_symbol_property_group} controls$: user.arc_get_symbol_property_controls(arc_symbol_property_group)
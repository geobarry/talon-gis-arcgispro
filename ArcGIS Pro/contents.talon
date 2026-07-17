os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-

# CONTENTS PANEL
list by Drawing Order: user.arc_contents_list_by('esri_mapping_DrawingOrderView')
list by Data Source: user.arc_contents_list_by('esri_mapping_DataSourceView')
list by Selection: user.arc_contents_list_by('esri_mapping_SelectionView')
list by Editing: user.arc_contents_list_by('esri_editing_EditingView')
list by Snapping: user.arc_contents_list_by('esri_mapping_SnappingView')
list by Labelling: user.arc_contents_list_by('esri_mapping_LabelingView')
list by Prospective Imagery: user.arc_contents_list_by('esri_mapping_ImageSpaceItemsView')


# CONTENTS PANEL LAYERS
layer select [<user.ordinals>] {user.arc_dynamic_layer}: user.arc_select_layer(arc_dynamic_layer, ordinals or 1)
layer copy {user.arc_dynamic_layer}: user.arc_copy_layer(arc_dynamic_layer,false)
layer expand {user.arc_dynamic_layer}: user.arc_expand_collapse_layer(arc_dynamic_layer,"expand")
layer collapse {user.arc_dynamic_layer}: user.arc_expand_collapse_layer(arc_dynamic_layer,"collapse")
layer {user.arc_layer_context_item}: user.arc_context_item(arc_layer_context_item)
layer {user.arc_dynamic_layer} {user.arc_layer_context_item}:
	user.arc_select_layer(arc_dynamic_layer)
	user.arc_context_item(arc_layer_context_item)
layer up: user.arc_drag_list_item("up")
layer down: user.arc_drag_list_item("down")
map properties: user.arc_context_item("Properties")
map projection: user.arc_map_coordinate_system()
^go to map$: user.arc_select_map_in_contents()
from talon import Module, Context, actions

mod=Module()

mod.list("arc_menu_heading","Main menu headings. Say 'menu {arc_menu_heading}' to open menu. Say 'arc help {arc_menu_heading} menu' for list of menu items.")
mod.list("arc_menu_heading_name","Main menu headings. Say 'menu {arc_menu_heading}' to open menu. Say 'arc help {arc_menu_heading} menu' for list of menu items.")

heading_dict={
    'Project':'Project',
    'Map':'a=esri_mapping_homeTab',
    'Layout':'a=(esri_layouts_homeTab|esri_layouts_ActivateMapTab)',
    'Insert':'a=esri_core_insertTab',
    'Analysis':'a=esri_core_analysisTab',
    'View':'a=esri_core_viewTab',
    'Edit':'a=esri_editing_EditingTab',
    'Imagery':'a=esri_datasourcesraster_imageryCoreTab',
    'Share':'a=esri_sharing_shareTab',
    'Help':'a=esri_core_helpTab',
    'Feature Layer':'a=esri_mapping_featureLayerAppearanceTab',
    'Labeling':'Labeling',
    'Data':'Data',
    'Linear Referencing':'Linear Referencing',
    'Tile Layer':'Tile Layer',
    'Fields':'a=esri_mapping_homeDesignViewTab',
    'Table':'a=esri_mapping_tableTab',
    'Design':'a=esri_layouts_compositeDesignTab',

    'Map Frame':'a=esri_layouts_FormatTab',
    'Legend':'a=esri_layouts_FormatTab',
    'Scale Bar':'a=esri_layouts_FormatTab',
    'Text':'a=esri_layouts_FormatTab',
    'Group':'Group',
    'Animation':'a=esri_mapping_animationTab',
    'Raster Layer':'a=esri_mapping_rasterLayerAppearanceTab',
    'North Arrow':'a=esri_layouts_FormatTab'
}

heading_name_dict={x:x for x in heading_dict.keys()}

arcgis_pro_ctx=Context()
arcgis_pro_ctx.lists["user.arc_menu_heading"] = heading_dict
arcgis_pro_ctx.lists["user.arc_menu_heading_name"] = heading_name_dict
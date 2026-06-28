from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax, ui as winui

mod = Module()

mod.list("arc_primary_symbology_control","control on the primary symbology panel")
mod.list("arc_primary_symbology","Primary symbology types in ArcGIS Pro")
mod.list("arc_symbol_property_group","assemble property group inside symbology tab")
mod.list("arc_color_symbol_control","specifications to get to a color symbol control")
mod.list("arc_symbol_control","specifications to get to a symbol control")
mod.list("arc_symbol_effect","effect that can be applied to symbols in symbology")

ctx=Context()

ctx.lists["user.arc_symbol_effect"] = {
    'Add control points':'Add control points effect',
    'Arrow':'Arrow effect',
    'Buffer':'Buffer effect',
    'Control measure line':'Control measure line effect',
    'Cut':'Cut effect',
    'Dash':'Dash effect',
    'Enclosing polygon':'Enclosing polygon effect',
    'Extension':'Extension effect',
    'Jog':'Jog effect',
    'Move':'Move effect',
    'Offset':'Offset effect',
    'Offset hatch':'Offset hatch effect',
    'Offset tangent':'Offset tangent effect',
    'Reverse':'Reverse effect',
    'Rotate':'Rotate effect',
    'Scale':'Scale effect',
    'Suppress':'Suppress effect',
    'Tapered polygon':'Tapered polygon effect',
    'Wave':'Wave effect',
    'Circular sector':'Circular sector effect',
    'Donut':'Donut effect',
    'Localizer feather':'Localizer feather effect',
    'Radial':'Radial effect',
    'Regular polygon':'Regular polygon effect',
}

ctx.lists["user.arc_symbol_property_group"] = {
    'Appearance':'Symbol, Appearance',
    'Halo':'Symbol, Halo',
    'Layer Appearance':'Layers, Appearance',
    'Position':'Layers, Position',
    'Rotation':'Layers, Rotation',
    'Offset Distance':'Layers, Offset Distance',
    'Output':'Layers, Output',
    'Structure Symbol':'Structure, Symbol',
    'Structure Layers':'Structure, Layers'
}

ctx.lists["user.arc_color_symbol_control"] = {
    'Color':'Symbol;Appearance;n=Color,c=DropDownColorPicker;n=Selected Color,c=ComboBox',
    'Fill Color':'Symbol;Appearance;n=Color,c=DropdownColorPicker;n=Selected Color,c=ComboBox',
    'Outline color':'Symbol;Appearance;n=Outline color,c=DropDownColorPicker;n=Selected Color,c=ComboBox',
    'Halo Color':'Symbol;Halo;n=Color,c=DropDownColorPicker;n=Selected Color,c=ComboBox',
    'Halo Outline color':'Symbol;Halo;n=Outline color,c=DropDownColorPicker;n=Selected Color,c=ComboBox',
}

ctx.lists["user.arc_symbol_control"] = {
    'Shape fill symbol':'Symbol;Appearance;n=Shape fill symbol,c=ComboBox',

    'Outline width':'Symbol;Appearance;n=Outline width,c=DoubleEditBox;n=Outline width,c=TextBox',
    'Line width':'Symbol;Appearance;n=Line width;n=Line width,c=TextBox',
    'Size':'Symbol;Appearance;n=Size,c=DoubleEditBox;n=Size,c=TextBox',
    'Enable scale based sizing':'Symbol;Appearance;n=Enable scale-based sizing,c=CheckBox',
    'Angle':'Symbol;Appearance;n=Angle,c=DoubleEditBoxWithDropDown',
    'Halo':'Symbol;Halo;n=,c=ComboBox',
    'Halo Outline width':'Symbol;Halo;n=Outline width,c=DoubleEditBox;n=Outline width,c=TextBox',
    'Halo size':'Symbol;Halo;n=Halo size,c=DoubleEditBox'
} | ctx.lists["user.arc_color_symbol_control"]
 
scroll_id = {
    "Symbol":".*BasicPropertiesScrollViewer",
    "Layers":".*LayersPropertiesScrollViewer",
    "Structure":""
}

@mod.action_class
class Actions:
    def control_primary_symbology(prop_str: str, action: str = ""):
        """Finds the given control within the symbology panel, 
           performs a given action on it and returns the element"""
        prop_seq_B = actions.user.get_property_sequence(prop_str)
        root = actions.user.window_root()
        prop_seq = [
        	[("class_name","FrameworkDockSite"),("automation_id","dockSite")],
        	[("class_name","DockHost"),("automation_id","dockSite.PART_DockHost")],
        	[("class_name","SplitContainer")],
        	[("class_name","SplitContainer")],
        	[("class_name","ToolWindowContainer")],
        	[("class_name","DockingWindowContainerTabItem"),("automation_id","esri_mapping_symbologyDockPaneTab")],
        	[("class_name","ToolWindow"),("automation_id","esri_mapping_symbologyDockPane")],
        	[("class_name","SymbologyDockPane")],
#        	[("class_name","ScrollViewer")],
        ]
        prop_seq += prop_seq_B
        el = actions.user.find_el_by_prop_seq(prop_seq,root,extra_search_levels = 4,verbose = True)
        if el and action != '':
            actions.user.act_on_element(el,action)
        return el
    def arc_symbology_tabs():
        """From within the symbology panel, tabs to either the gallery or properties tab"""
        prop_list = ["OR",[
                        ["AND",[("name","Properties"),("class_name","ListBoxItem")]],
                        ["AND",[("name","Gallery"),("class_name","ListBoxItem")]]
                    ]]
        actions.user.key_to_matching_element("tab",prop_list,delay = 0.05)
    def arc_import_symbology():
        """Navigates to the import symbology tool. Assumes a layer is selected and the symbology panel is open"""
        actions.user.arc_select_panel("Symbology")
        prop_seq = [
                [("automation_id","dockSite")],
                [("automation_id","dockSite.PART_DockHost")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq)
        print(f'1st el: {el}')
        if el:
            prop_list = [("automation_id","esri_mapping_symbologyDockPaneTab")]
            el = actions.user.matching_descendant(el,prop_list,4)
            print(f'2nd el: {el}')
            if el:
                prop_list = [("automation_id","Symbology_BurgerButton")]
                el = actions.user.matching_descendant(el,prop_list,3)
                print(f'3rd el: {el}')
                if el:
                    el.expandcollapse_pattern.expand()
                    # actions.sleep(2)
                    actions.key("down enter")
                    actions.sleep(1)
                    prop_list = [("name","Symbology Layer")]#,("class_name","Textbox")]
                    actions.user.key_to_matching_element("tab",prop_list)
                    actions.sleep(0.5)
                    actions.key("alt-down")
    def arc_select_primary_symbology(symbology_type: str = ""):
        """Selects the primary symbology combo box in the symbology panel"""
        tool_window = actions.user.arc_tool_window("Symbology")
        if tool_window:
            prop_seq = [
    #            [("class_name","SymbologyDockPane")],
                [("name",".*symbology.*"),("class_name","TextBlock")]
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,tool_window)
            print(f'el name***: {actions.user.el_prop_val(el,"name")}')
            if el:
                # make sure element name is "Primary symbology"
                name = actions.user.el_prop_val(el,'name')
                print(f'name: {name}')
                if name != "Primary symbology":
                    # use the back button to get to where we want to go
                    prop_list = [("automation_id","Symbology_BackButton")]
                    button = actions.user.find_el_by_prop_seq([prop_list],tool_window,verbose = True)
                    print(f'button: {button}')
                    if button:
                        actions.user.act_on_element(button,'invoke')
                        el = actions.user.find_el_by_prop_seq(prop_seq,tool_window)
                    else:
                        return 
                # Select Combo Box With Primary Symbology
                prop_list = [("name","Selected primary symbology"),("class_name","ComboBox")]
                el = actions.user.matching_descendant(tool_window,prop_list,2)
                print(f'el: {el}')
                if el:
                    actions.user.act_on_element(el,"select")
                    actions.user.act_on_element(el,"expand")
                    if symbology_type != "":
                        actions.key("home")
                        prop_list = [("name",symbology_type)]
                        if not actions.user.element_match(actions.user.safe_focused_element(),prop_list):
                            actions.user.key_to_matching_element("down",prop_list)
                        actions.key("enter")
    def arc_symbol_tab(gallery_or_properties: str):
        """navigate to symbol gallery or properties and returns DockPane"""
        print("FUNCTION: arc_symbol")
        # get tool window
        tool_window = actions.user.arc_tool_window("Symbology")
        print(f'tool_window: {tool_window}')
        if not tool_window:
            print("Unable to find Symbology tool window")
            return 
        else:
            # get DockPane
            DockPane = actions.user.matching_child(tool_window,[("class_name","SymbologyDockPane")])
            # see if we are already in Advanced symbology options
            in_advanced_symbology = False
            prop_list = [("name","Advanced symbology options")]
            el = actions.user.matching_child(DockPane,prop_list)
            if el:
                if "LegacyIAccessible" in el.patterns:
                    legacy_state = el.legacyiaccessible_pattern.state
                    print(f'legacy_state: {legacy_state}')
                    if legacy_state == 0:
                        in_advanced_symbology = True
                        print(f"Already in Advanced symbology options")
            if not in_advanced_symbology:
                print("Not in Advanced symbology options - looking at primary symbology")
                # If Single Symbol, automatically navigate to Advanced symbology options
                # Determine symbology type
                prop_list = [("name","Selected primary symbology"),("class_name","ComboBox")]
                el = actions.user.matching_descendant(DockPane,prop_list,2)
                if not el:
                    print("Can't find primary symbology combo box")
                    return
                else:
                    if not "Selection" in el.patterns:
                        print("Primary symbology combo box has no selection pattern")
                        return
                    else:
                        sel_el = el.selection_pattern.selection[0]
                        if not sel_el:
                            print("Primary symbology box has no selected element")
                            return 
                        else:
                            if not sel_el.name == "Single Symbol":
                                print("Primary symbology is not Single Symbol - exiting")
                                return 
                            else:
                                print("Primary symbology is Single Symbol - opening Advanced symbology options")
                                # Invoke single symbol renderer button
                                prop_list = [("automation_id","SingleSymbolRendererCurrentSymbolButton")]
                                el = actions.user.matching_descendant(DockPane,prop_list,2)
                                if el:
                                    actions.user.act_on_element(el,"invoke")
                                    actions.sleep(0.1)

            if not DockPane:
                print("Unable to locate SymbologyDockPane")
                return 
            else:
                # click on either gallery or properties
                prop_list = [("name",gallery_or_properties),("class_name","ListBoxItem")]
                el = actions.user.matching_descendant(DockPane,prop_list,2)
                actions.user.act_on_element(el,'select')
                
                return DockPane
    def arc_symbol_property_tab(prop_tab: str):
        """navigates to property tab and returns DockPane"""
        DockPane = actions.user.arc_symbol_tab("properties")
        print(f'DockPane: {DockPane}')
        if DockPane:
            prop_seq = [
                [("automation_id","SymbolGallery_Tabs")],
                [("class_name","ListBox")],
                # [("class_name","ListBox"),("automation_id","SymbolGallery_GalleryPropertiesHeader")],
                [("class_name","ListBoxItem"),("name",prop_tab)]
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,DockPane,verbose = True)
            if el:
                global scroll_id
                actions.user.act_on_element(el,"select")
                # get container with control groups and controls
                prop_seq = [
                    [("class_name","TabControl")],
                    [("class_name","TabControl")],
                    [("class_name","ScrollViewer"),("automation_id",scroll_id[prop_tab])],
                ]
                scroll_viewer = actions.user.find_el_by_prop_seq(prop_seq,DockPane,verbose = True)
                if scroll_viewer:
                    # collapse all control groups
                    prop_list=[("class_name","Expander")]
                    children=actions.user.matching_children(scroll_viewer,prop_list)
                    if children:
                        for child in children:
                            actions.user.act_on_element(child,'collapse')
        return DockPane
    def arc_symbol_property_group(prop_tab_and_group: str):
        """navigates to and returns property group expander"""
        print("FUNCTION: arc_symbol_property_group")
        prop_tab,prop_grp = prop_tab_and_group.split(",")
        prop_tab = prop_tab.strip()
        prop_grp = prop_grp.strip()
        DockPane = actions.user.arc_symbol_property_tab(prop_tab)

        if DockPane:
            global scroll_id
            # get container with control groups and controls
            prop_seq = [
                [("class_name","TabControl")],
                [("class_name","TabControl")],
                [("class_name","ScrollViewer"),("automation_id",scroll_id[prop_tab])],
            ]
            scroll_viewer = actions.user.find_el_by_prop_seq(prop_seq,DockPane,verbose = True)
            if scroll_viewer:
                # collapse all control groups except target, expand target
                prop_list=[("class_name","Expander")]
                children=actions.user.matching_children(scroll_viewer,prop_list)
                if children:
                    trg=None
                    prop_list=[("name",prop_grp)]
                    for child in children:
                        if actions.user.element_match(child,prop_list):
                            trg=child
                        else:
                            actions.user.act_on_element(child,'collapse')
                    if trg:
                        actions.user.act_on_element(trg,'expand')
                    return trg
    def arc_get_symbol_property_controls(prop_tab_and_group: str):
        """Compiles names and classes of symbol controls"""
        print("FUNCTION: arc_get_symbol_property_controls")
        prop_tab,prop_grp = prop_tab_and_group.split(",")
        prop_tab = prop_tab.strip()
        prop_grp = prop_grp.strip()        
        expander = actions.user.arc_symbol_property_group(prop_tab_and_group)
        if expander:
            item = []
            for child in expander.children:
                class_name = actions.user.el_prop_val(child,"class_name")
                if class_name != "TextBlock":
                    name = actions.user.el_prop_val(child,"name")
                    if name != prop_grp:
                        item.append(f'{name}: {",".join([prop_tab,prop_grp,name,class_name])}')
            clip.set_text("\n".join(item))
    def arc_symbol_control(ctrl_specs: str):
        """navigate to a particular symbol control"""
        # PARSE ctrl_specs
        print(f'ctrl_specs: {ctrl_specs}')
        val = [x.strip() for x in ctrl_specs.split(";")]
        print(f'val: {val}')
        prop_tab,prop_grp = val[0],val[1]
        prop_seq_str = val[2:]
        prop_seq = [actions.user.get_property_list(x) for x in prop_seq_str]
        print(f'prop_seq_str: {prop_seq_str}')
        
        # OBTAIN EXPANDER
        expander = actions.user.arc_symbol_property_group(",".join([prop_tab,prop_grp]))
        if not expander:
            print("arc_symbol_control could not find expander")
        else:
            el=actions.user.safe_focused_element()
            status = actions.user.el_prop_val(el,'expand_collapse_state')
            print(f'status: {status}')
            el = actions.user.find_el_by_prop_seq(prop_seq,expander,verbose=False)
            # This often seems to require more time
            if not el:
                stopper=actions.user.stopper(sec_lim = 1)
                while not el and not stopper.over():
                    actions.sleep(0.1)
                    el = actions.user.find_el_by_prop_seq(prop_seq,expander,verbose=True)
            print(f'looking for {prop_seq}\n el: {el}')
            
            if el:
                # some controls will have children that needed be accessed
                pattern_list = actions.user.el_prop_val(el,'patterns')
                print(f'pattern_list: {pattern_list}')
                if pattern_list:
                    if 'ExpandCollapse' in pattern_list:
                        actions.user.act_on_element(el,'expand')
                    else:
                        actions.user.act_on_element(el,"select")
        
    def arc_symbol_assign_color(ctrl_specs: str, color: str):
        """navigates to color symbol control and a science color"""
        # navigate to and expand color combo box
        actions.user.arc_symbol_control(ctrl_specs)
        # make sure color combo box is selected
        prop_list=[("name","Selected Color"),("control_type","ComboBox")]
        el=actions.user.wait_for_element(prop_list)
        print(f'el: {el}')
        if el:
            # make sure combo box is expanded
            status=actions.user.el_prop_val(el,'expand_collapse_state')
            if status == "Expanded":
                # navigate to and invoke Color Properties... button
                prop_list=[("name","Color Properties...")]
                actions.user.key_to_matching_element("tab",prop_list)
                el=actions.user.wait_for_element(prop_list)
                if el:
                    # invoking doesn't work so press enter key
                    actions.key("enter")
                    # wait for dialog Color Editor to appear
                    prop_list=[("name","Color Editor")]
                    el=actions.user.wait_for_element(prop_list)
                    if el:
                        # tab to the hex value editor
                        prop_list=[("automation_id","ColorEditorHexValue.*")]
                        actions.user.key_to_matching_element("tab",prop_list)
                        el=actions.user.wait_for_element(prop_list)
                        if el:
                            # enter value
                            actions.insert(color)
                            # shift tab to (1) validate entry, and (2) place focus on transparency
                            actions.key("shift-tab")
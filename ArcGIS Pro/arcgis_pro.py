from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax
import re, time

mod = Module()

mod.list("arc_panel","panels that can be accessed with standard keyboard shortcut")
mod.list("arc_button","buttons that can be accessed with standard keyboard shortcuts in ArcGIS Pro")
mod.list("arc_catalog_group","groups of items in the catalog pane")
mod.list("arc_layer_context_item","menu items available when right clicking on map layer")
mod.list("arc_contents_map_context_item","automation_id's for items in context menu when you right click map in them Table of Contents")
mod.list("arc_ribbon_heading","Names of main ribbon headings")
mod.list("arc_ribbon_item","Sequence of elements to access each item on the ribbon")
mod.list("arc_contents_list_style","List style for contents panel")

mod.list("arc_field_name","the name of a field for definition queries and attribute selection")

mod.list("arc_parameter","property list for parameter in geoprocessing tool window")
mod.list("compass_direction","Compass direction")
mod.list("arc_dynamic_panel","currently accessible panels")
mod.list("arc_dynamic_layer","layers_in_the_table_of_contents")
mod.list("arc_dynamic_toolbox","toolboxes in geoprocessing pane")
mod.list("arc_geoprocessing_tool","geoprocessing tool name for search")

compass_diffs = {
    "north": (0,-1),
    "south": (0,1),
    "east": (1,0),
    "west": (-1,0)
}

global panels
global layers
global layout_wd 
layout_wd = -1
global layout_ht 
layout_ht = -1

ctx = Context()

# HELPER FUNCTIONS
def ensure_focus():
    """ watch out for the windows airspace popup that steals the focus!!"""
    actions.key("esc:5")
    w = ui.active_window()
    root = ui.active_window().element
    if root.automation_id == "AirspacePopup":
        actions.user.switcher_focus("ArcGIS Pro")
        root = ui.active_window().element     
def prop_cond(talon_list_text):
    """creates a property tuple using the name property unless there is an equal sign"""
    if "=" in talon_list_text:
        prop_val = talon_list_text.split("=")
        return (prop_val[0],prop_val[1])
    else:
        return ("name",talon_list_text)
def remove_underscores(prop_name: str, val: str):
    if prop_name.lower() == "name":
        return val.replace("_","")
    else:
        return val
def expand_ribbon():
    """Returns true if ribbon needed to be expanded"""
    root = actions.user.window_root()
    prop_seq = [
        [("class_name","Ribbon")],
    ]
    el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
    state = el.expandcollapse_pattern.state
    if state == "Collapsed":
        actions.user.act_on_element(el,"expand")        
        return True
    else:
        return False
def collapse_ribbon():
    print(f"FUNCTION collapse_ribbon")
    root = actions.user.window_root()
    prop_seq = [
        [("class_name","Ribbon")],
    ]
    el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
    state = el.expandcollapse_pattern.state
    print(f'state: {state}')
    if state == "Expanded":
        actions.user.act_on_element(el,"collapse")
def get_leaves(root,prop_name,branch_val,leaf_val):
    r = []
    if root:
        children = actions.user.el_prop_val(root,'children')
        if children:
            for child in children:
                val = actions.user.el_prop_val(child,prop_name)
                if re.match(leaf_val,val) != None:
                    r.append(child)
                if re.match(branch_val,val) != None:
                    r += get_leaves(child,prop_name,branch_val,leaf_val)
    return r
def get_layers():
    tool_window = actions.user.arc_tool_window("Contents")
    if tool_window:
        prop_seq = [
            [("class_name","ContentsDockPane")],
            [("class_name","TOCControl")],
            [("class_name","TreeView"),("automation_id",".*TOC")]
        ]
        TreeView = actions.user.find_el_by_prop_seq(prop_seq,tool_window,verbose = False)
        if TreeView:
            leaf_val = ".*TOCItem_.*"
            branch_val = ".*TOCItem_(Map|Group|Layout).*"
            leaf_val = re.compile(f"^{leaf_val}$",re.IGNORECASE)
            branch_val = re.compile(f"^{branch_val}$",re.IGNORECASE)
            leaves = get_leaves(TreeView,"automation_id",branch_val,leaf_val)
            return leaves
def get_panels():
    start_time=time.perf_counter()

    app = ui.active_app()
    ws = []
    for x in app.windows():
        if x.title != "" and not x.hidden:
            ws.append(x)
        if x.hidden:
            break
    w_n = len(ws)

    finish_time=time.perf_counter()
    w_time=finish_time - start_time
    start_time=time.perf_counter()

    leaf_names = [".*TabItem",".*ToolWindow"]
    branch_names = [".*Container","Workspace","DockHost","FrameworkDockSite","Window"]
    # leaf_prop = [("class_name",f"({'|'.join(leaf_names)})")]
    # branch_prop = [("class_name",f"({'|'.join(branch_names)})")]
    leaf_val = f"({'|'.join(leaf_names)})"
    branch_val = f"({'|'.join(branch_names)})"
    leaf_val = re.compile(f"^{leaf_val}$",re.IGNORECASE)
    branch_val = re.compile(f"^{branch_val}$",re.IGNORECASE)
    leaf_lists = [get_leaves(w.element,"class_name",branch_val,leaf_val) for w in ws]
    # leaf_lists = [get_leaves(w.element,branch_prop,leaf_prop) for w in ws]
    leaves = [item for sublist in leaf_lists for item in sublist]

    finish_time=time.perf_counter()
    leaf_time=finish_time - start_time
    print(f'w_time: {w_time}')
    print(f'leaf_time: {leaf_time}')
    print(f'len(leaves): {len(leaves)}')
    return leaves

                
@ctx.dynamic_list("user.arc_dynamic_layer")
def arc_dynamic_layer(_) -> dict[str,str]:
    """layers currently in table of contents"""
    global layers
    layers = get_layers()
    if layers:
        name_list = [layer.name for layer in layers]
        out = actions.user.create_spoken_forms_from_list(name_list)
        return out
    
@ctx.dynamic_list("user.arc_dynamic_panel")
def arc_dynamic_panel(_) -> dict[str,str]:
    """currently open panels, maps, tables..."""
    # it looks like we can assume that hidden windows all come after visible windows
    # and we can save a tiny fraction of a second by not requesting title and hidden from all windows!
    global panels
    panels = get_panels()
    name_list = [el.name for el in panels]
    print(f'name_list: {name_list}')
    out = actions.user.text_to_spoken_forms(name_list)
    return out

@ctx.dynamic_list("user.arc_dynamic_toolbox")            
def arc_dynamic_toolbox(_) -> str:
    print("FUNCTION: arc_dynamic_toolbox")
    tool_window = actions.user.arc_tool_window("Geoprocessing")
    print(f'tool_window: {tool_window}')
    if tool_window:
        r = []
        # later add code here to navigate to toolbox pane if not already opened
        prop_seq = [
            [("class_name","GPDocPaneView")],
            [("class_name","MainPageView")],
            [("class_name","TreeView")]
        ]
        TreeView = actions.user.find_el_by_prop_seq(prop_seq,tool_window,verbose = True)
        print(f'TreeView: {TreeView}')
        el_list = actions.user.matching_children(TreeView,[("class_name","TreeViewItem")])
        if el_list:
            for el in el_list:
                print(f'el: {el.name}')
                if el.name != "ArcGIS.Desktop.GeoProcessing.ToolInfoViewModel":
                    r.append(el.name[:-6])
            return "\n\n".join(r)
@mod.capture(rule="{user.arc_panel}|<user.text>")
def arc_panel(m) -> str:
    """a predefined panel or spoken text"""
    if hasattr(m,"arc_panel"):
        return m.arc_panel
    else:
        return m.text

@mod.capture(rule="<user.real_number> (north|south|east|west) <user.real_number> (north|south|east|west)")
def arc_coordinate(m) -> str:
    """a single coordinate expressed as a string of '<easting>,<northing>'"""
    print(m)
    txt = str(m)
    txt_list = txt.split(" ")
    print(f'txt_list: {txt_list}')
    r = ''
    idx_list = [1,3]
    easting = None
    northing = None
    for idx in idx_list:
        if txt_list[idx] == "east":
            easting = float(txt_list[idx - 1])
        if txt_list[idx] == "west":
            easting = -1 * float(txt_list[idx - 1])
        if txt_list[idx] == "north":
            northing = float(txt_list[idx - 1])
        if txt_list[idx] == "south":
            northing = -1 * float(txt_list[idx - 1])
    print(f'easting: {easting}')
    print(f'northing: {northing}')
    if easting == None or northing == None:
        print("no easting or northing")
        return None
    else:
        print("else...")
        return f"{easting},{northing}"

@mod.action_class
class Actions:
    def arc_ribbon_heading_element(heading: str):
        """Obtain ribbon heading windows accessibility element"""
        # get parent element
        ensure_focus()
        root = actions.user.window_root()
        if heading == "Project":
            prop_seq = [
                [("class_name","Ribbon")],
                [("class_name","RibbonApplicationButton"),("name",heading)]
            ]    
        else:
            prop_seq = [
                [("class_name","Ribbon")],
                [("class_name","RibbonTabHeaderItemsControl")],
                [("class_name","RibbonTabHeader"),("name",heading)]
            ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        return el
    def arc_open_ribbon(heading: str):
        """Opens the menu; use talon list user.arc_ribbon_heading"""
        # Try to ensure that the current focus is on the main application
        ensure_focus()
        # obtain the ribbon element
        root = actions.user.window_root()
        prop_seq = [
			[("class_name","Ribbon")],
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        if el:
            # determine if the ribbon is showing or hidden
            state = el.expandcollapse_pattern.state
            # get ribbon heading element
            el = actions.user.arc_ribbon_heading_element(heading)
            if state == "Collapsed" and heading != "Project":
                actions.user.act_on_element(el,"click")
            actions.user.act_on_element(el,"select")
            if heading == "Project":
                actions.key("enter")
            return el
    def arc_ribbon_item(seq: str):
        """Returns element on ribbon; use {user.arc_ribbon_item}"""
        ensure_focus()
        print(f'seq: {seq}')
        # make sure ribbon is expanded
        need_to_collapse = expand_ribbon()
        seq = seq.split(",")
        el = actions.user.arc_ribbon_heading_element(seq[0])
        elapsed_sec=0
        if el:
            actions.user.act_on_element(el,"select")
            prop_seq = [actions.user.get_property_list(s) for s in seq[1:] if s != '']
            for prop_list in prop_seq:
                print(f'prop_list: {prop_list}')
                pattern_list=actions.user.el_prop_val(el,'patterns')
                if pattern_list:
                    if "ExpandCollapse" in pattern_list:
                        actions.user.act_on_element(el,"expand")
                    start_time=time.perf_counter()
                    # this is much faster:
                    el=actions.user.find_el_by_prop_seq([prop_list],el)
                    # el = actions.user.matching_descendant(el,prop_list,1,3)
                    finish_time=time.perf_counter()
                    elapsed_sec += finish_time - start_time
                    if not el:
                        print(f"could not find element {prop_list}")
                        break
        print(f'elapsed_sec: {elapsed_sec}')
        return el,need_to_collapse
    def arc_call_ribbon_item(seq: str):
        """Performs default action on ribbon item"""
        el,need_to_collapse = actions.user.arc_ribbon_item(seq)
        # If the button is disabled, the element will be None
        if el:
            # make sure element has been selected
#            actions.user.act_on_element(el,"select")
            prop_list=[("name",seq.split(",")[-1])]
            print(f'arc_call_ribbon_item: el: {el}')
            
            pattern_list = actions.user.el_prop_val(el,'patterns')
            if pattern_list:
                if "Invoke" in pattern_list:
                    actions.user.act_on_element(el,"invoke")
                    if need_to_collapse:
                        collapse_ribbon()
                elif "ExpandCollapse" in pattern_list:
                    actions.user.act_on_element(el,"expand")
                else:
                    actions.user.act_on_element(el,"hover")
                    actions.user.act_on_element(el,'select')
    def arc_get_ribbon_items(heading: str):
        """Creates text for a talon list of ribbon items"""
        ribbon_heading = actions.user.arc_ribbon_heading_element(heading)
        actions.user.act_on_element(ribbon_heading,"select")
        r = []
        def append_item(item, seq):
            new_seq = seq + [item.name]
            if len(item.children) > 0:
                for child in item.children:
                    append_item(child,new_seq)
            elif item.name != "":
                r.append(new_seq)
        append_item(ribbon_heading,[])
        r = [f"{x[0]} {x[-1]}: {','.join(x)}" for x in r]
        clip.set_text("\n".join(r))
    def arc_tool_window(name: str):
        """Need to make sure catalog panel is visible before calling this"""
        # let's go from bottom up
        print("FUNCTION: actions.user.arc_tool_window")
        el = actions.user.safe_focused_element()
        if el:
            prop_list = [("name",name + ".*"),("class_name",".*ToolWindow")]        
            tool_window = actions.user.matching_ancestor(el,prop_list)
            if tool_window:
                return tool_window
            else:
                tool_window = actions.user.arc_select_panel(name)
                if tool_window:
                    return tool_window
    def arc_nav_toolbox(toolbox_name: str):
        """Navigate to a toolbox"""
        print("FUNCTION: arc_nav_toolbox")
        tool_window = actions.user.arc_tool_window("Geoprocessing")
        print(f'tool_window: {tool_window}')
        if tool_window:
            # later add code here to navigate to toolbox pane if not already opened
            prop_seq = [
                [("class_name","GPDocPaneView")],
                [("class_name","MainPageView")],
                [("class_name","TreeView")],
                [("name", toolbox_name)]
            ]
            TreeViewItem = actions.user.find_el_by_prop_seq(prop_seq,tool_window,verbose = True)
            print(f'TreeViewItem: {TreeViewItem}')
            if TreeViewItem:
                actions.user.act_on_element(TreeViewItem,"expand")
                children = actions.user.matching_children(TreeViewItem,[("class_name","TreeViewItem")])
                if children:
                    last_child = children[-1]
                    if last_child:
                        actions.user.act_on_element(last_child,"scroll_into_view")
                actions.user.act_on_element(TreeViewItem,"scroll_into_view")
    def arc_select_panel(panel_name: str, got_panels: bool = False):
        """Selects a panel, tab, or similar"""
        print(f'panel_name: {panel_name}')
        global panels
        if not got_panels:
            panels = get_panels()
        prop_list = [("name",panel_name)]
        el = None
        for panel in panels:
            if actions.user.element_match(panel,prop_list):
                el = panel
                break
        if el:
            def perform_post_processing(el):
                if panel_name == "Catalog":
                    # set focus on selected item
                    prop_seq = [
                        [("class_name","ProjectDockPane")],
                        [("automation_id","MainTreeView")]
                    ]
                    el = actions.user.find_el_by_prop_seq(prop_seq,el,verbose = True)
                    if el:
                        pattern = el.selection_pattern
                        if pattern:
                            sel_el = pattern.selection
                            if sel_el:
                                actions.user.act_on_element(sel_el[0],"select")
            actions.user.act_on_element(el,"select")
            prop_list = [("class_name",".*Window")]
            child = actions.user.matching_child(el,prop_list)
            if child:
                actions.user.act_on_element(child,"invoke")
                actions.user.act_on_element(child,"select")
                # take further action depending on panel
                perform_post_processing(child)
                return child
            else:
                # take further action depending on panel
                print(f'el: {el}')
                perform_post_processing(el)
                return el
    def arc_tab_to_layers():
        """presses the tab key to get to the layer list area"""
        # make sure Contents panel is selected
        prop_list = [("name","Contents"),("class_name",".*ToolWindow")]
        el = actions.user.safe_focused_element()
        if not actions.user.matching_ancestor(el,prop_list):
            actions.user.arc_select_panel("Contents")
        if actions.user.wait_for_matching_ancestor(prop_list):
            print(f"FUNCTION: arc_tab_to_layers")
            actions.user.key_to_matching_element("tab",["OR",[("class_name","TreeView"),("class_name",  "TreeViewItem")]],escape_key = "esc")
    def arc_tab_to_layer(layer_name: str):
        """presses the down key to get to the specified layer"""
        actions.user.key_to_matching_element("down",[("name",f"{layer_name}.*")])
        actions.user.jiggle("down")
    def arc_select_layer(layer_name: str,got_layers: bool = False):
        """selects given layer using windows automation"""
        global layers
        if not got_layers:
            layers = get_layers()
        layer_dict = {el.name:el for el in layers}
        el = layer_dict[layer_name]
        if el:
            actions.user.act_on_element(el,"select")
            actions.key("up down")
            prop_list = [("name",layer_name)]
            el = actions.user.wait_for_element(prop_list)
            print(f'el: {el}')
            return el
    def arc_copy_layer(layer_name: str, got_layers: bool = False):
        """Selects layer and then copies it into containing map"""
        layer_el = actions.user.arc_select_layer(layer_name,got_layers)
        if layer_el:
            # copy 
            actions.key("ctrl-c")
            # obtain map element
            prop_list = [("automation_id","mappingTOCItem_map.*")]
            container = actions.user.matching_ancestor(layer_el,prop_list)
            if container:
                actions.user.act_on_element(container,'select')
                container = actions.user.wait_for_element(prop_list)
                if container:
                    actions.key("ctrl-v")
    def arc_color_editor_window():
        """Returns the color editor window"""
        # make sure selected combo box is open
        el = actions.user.safe_focused_element()
        prop_list = [("name",".*Color.*"),("control_type","ComboBox")]
        if not actions.user.element_match(el,prop_list):
            return
        state = actions.user.el_prop_val(el,'expand_collapse_state')
        print(f'state: {state}')
        if state == "Collapsed":
            actions.user.act_on_element(el,'expand')
        # click on color properties button
        root = actions.user.window_root()
        print(f'root: {root}')
        prop_seq = [
        	[("class_name","Popup"),("control_type","Window")],
        	[("class_name","ColorPalette"),("control_type","Custom")],
        	[("name","Color Properties..."),("class_name","Button"),("control_type","Button")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        print(f'el: {el}')
        if el:
            actions.user.act_on_element(el,'click')
            # wait for color editor window to open
            prop_list = [("name","Color Editor")]
            w = actions.user.wait_for_element(prop_list)
            return w
    def arc_select_color_transparency(val: int):
        """selects a color given that the color dropdown already is open"""
        w = actions.user.arc_color_editor_window()
        if w:
            prop_seq = [
                [("control_type","Custom"),("automation_id","ColorEditorControl")],
                [("control_type","Spinner"),("automation_id","ColorEditorHorizontalPercentDoubleEditBox")],
                [("control_type","Edit")]
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,w,verbose = True)
            print(f'el: {el}')
            if el:
                actions.user.set_el_prop_val(el,"value",str(val))
                val_new = actions.user.el_prop_val(el,'value')
                print(f'val_new: {val_new}')
                if val_new == val:
                    print("got it!")
                    actions.user.arc_tab_to_button("OK",True)
    def arc_select_color(hex_code: str):
        """selects a color given that the color dropdown already is open"""
        w = actions.user.arc_color_editor_window()
        if w:
            prop_seq = [
                [("control_type","Custom"),("automation_id","ColorEditorControl")],
                [("control_type","Edit"),("automation_id","ColorEditorHexValue2")]
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,w,verbose = True)
            print(f'el: {el}')
            if el:
                actions.user.set_el_prop_val(el,"value",hex_code)
                val = actions.user.el_prop_val(el,'value')
                print(f'val: {val}')
                if val == hex_code:
                    print("got it!")
                    actions.user.arc_tab_to_button("OK",True)
    def arc_expand_collapse_layer(layer_name: str,expand_collapse: str):
        """attempts to expand or collapse the given layer and keep it selected"""
        el = actions.user.arc_select_layer(layer_name)
        if el:
            if expand_collapse == "expand":
                actions.key("right")
            else:
                actions.key("left")
            prop_list = [("name",f"^(?!.*{layer_name}).*")]
            dummy = actions.user.wait_for_element(prop_list,time_limit = 2)
            print(f'dummy: {dummy}')
            if dummy:
                actions.user.act_on_element(el,'select')
    def arc_select_catalog_group(group_name: str):
        """Selects a group heading within the catalog panel"""
        print("FUNCTION: arc_select_catalog_group")
        tool_window = actions.user.arc_tool_window("Catalog")
        print(f'tool_window: {tool_window}')
        if tool_window:
            group_list = ["Maps","Toolboxes","Notebooks","Databases","Layouts","Styles","Folders","Locators"]
            prop_seq = [
                [("class_name","ProjectDockPane")],
                [("class_name","TreeView")],
            ]
            TreeView = actions.user.find_el_by_prop_seq(prop_seq,tool_window,verbose = False)
            print(f'TreeView: {TreeView}')
            if TreeView:
                sel_el = None
                for el in TreeView.children:
                    name = el.name
                    print(f'name: {name}')
                    try:
                        status = el.expandcollapse_pattern.state
                        print(f'{el.name} status: {status}')
                    except:
                        print(f"getting error trying to get expand state on {el}")
                    if name == group_name:
                        sel_el = el
                    elif name != group_name and status == "Expanded":
                        el.expandcollapse_pattern.collapse()
                print(f'sel_el: {sel_el}')
                if not sel_el:
                    for el in TreeView.children:
                        if name == group_name:
                            sel_el = el            
                sel_el.expandcollapse_pattern.expand()
    def arc_tab_to_button(button_name: str, do_click: bool = False):
        """Presses tab to reach button and then presses enter"""
        prop_list = actions.user.get_property_list(f"{button_name}.*")
        el = actions.user.key_to_matching_element("tab", prop_list,
            avoid_cycles = False,
            verbose = True)
        if do_click:
            if el:
                actions.user.act_on_element(el,'click')
    def arc_context_item(item_str: str):
        """Navigates to item using keyboard keys"""
        actions.key("menu")
        el = actions.user.safe_focused_element()
        print(f'FUNCTION arc_context_item el: {el}')

        item_list = item_str.split(",")
        print(f'item_list: {item_list}')
        root = actions.user.window_root()
        prop_seq = [
            [("name",""),("class_name","Popup")],
        ]
        menu = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
        def scroll_menu(menu, up: bool = True):
            if menu:
                rect = actions.user.el_prop_val(menu,'rect')
                if rect:
                    # We are going to have to use the mouse to move up and down in the menu
                    x = int(rect.left + rect.width/2)
                    if up:
                        print(f"scrolling up...")
                        y = int(rect.top + 20)
                    else:
                        print("scrolling down...")
                        y = int(rect.top + rect.height - 40)
                    ctrl.mouse_move(x,y)
        for i in range(len(item_list)):
            # actions.sleep(0.5)
            # el = actions.user.safe_focused_element()
            el = actions.user.safe_focused_element()
            print(f'arc_context_item: el: {el}')
            print(f'el class_name: {actions.user.el_prop_val(el,"class_name")}')
            prop_list = [("class_name","Pro.*Menu.*")]
            
            el = actions.user.wait_for_element(prop_list)
            prop_list = [("name",item_list[i])]
            actions.user.key_to_matching_element("up",prop_list,mod_func = remove_underscores,limit = 25,verbose = False)
            el = actions.user.safe_focused_element()
            if not actions.user.element_match(el,prop_list,mod_func = remove_underscores):
                scroll_menu(menu,True)
                print(f'prop_list: {prop_list}')
                actions.user.key_to_matching_element("up",prop_list,mod_func = remove_underscores,limit = 25,verbose = False)
                el = actions.user.safe_focused_element()
                if not actions.user.element_match(el,prop_list,mod_func = remove_underscores):
                    scroll_menu(menu,False)
                    el = actions.user.safe_focused_element()
                    if not actions.user.element_match(el,prop_list,mod_func = remove_underscores):
                        return 
            print(f'context menu item: {el}')
            if i < len(item_list) - 1:
                if actions.user.element_match(el,prop_list,mod_func = remove_underscores):
                    print("pressing right button")
                    actions.sleep(0.1)
                    actions.key("right")
                else:
                    print(f'prop_list: {prop_list}')
                    break
    def arc_key_to_element(key: str, 
                                prop_str: str, 
                                ordinal: int=1, 
                                verbose: bool = False):
        """Remove underscores before using key to matching element"""
        prop_list = actions.user.get_property_list(prop_str)
        actions.user.key_to_matching_element(
            key,prop_list,
            ordinal = ordinal,
            verbose = verbose,
            mod_func = remove_underscores            
        )
    def arc_contents_nav_to_layer_item(up_or_down: str = "down",layer_type: str = ""):
        """navigates the contents panel to the next/previous layer item"""
        print("ARC_CONTENTS_NAV_TO_LAYER_ITEM")
        # Error Checking
        if up_or_down.lower() not in ["up","down"]:
            return 
        if layer_type not in ["FeatureLayer","RasterLayer","VectorTileLayer","TiledServiceLayer"]:
            layer_type = ""
        # first navigate to a table of contents item
        prop_list = [("automation_id",".*TOCItem.*")]
        actions.user.key_to_matching_element("tab",prop_list)
        # press key at least once
        actions.key(up_or_down)
        # navigate to next layer item
        if layer_type == "":
            prop_list = ["OR",[
                ("automation_id","mappingTOCItem_FeatureLayer.*"),
                ("automation_id","mappingTOCItem_RasterLayer.*"),
                ("automation_id","mappingTOCItem_VectorTileLayer.*"),
                ("automation_id","mappingTOCItem_TiledServiceLayer.*"),
            ]]
        else:
            prop_list = [("automation_id",f"mappingTOCItem_{layer_type}.*")]
        actions.user.key_to_matching_element(up_or_down,prop_list)
    def arc_contents_list_by(contents_list_style: str):
        """Chooses display option for Contents Pane; options are stored in arc_contents_list_style"""
        # first make sure the focus is on the contents panel
        actions.user.arc_select_panel("Contents")
        # press tab until we get to a ListBoxItem
        prop_list = [("class_name","ListBoxItem")]
        actions.user.key_to_matching_element("tab",prop_list)
        # press the Home key to get all the way to the left
        actions.key("home")
        # press right key until we get to designated style
        prop_list = [("automation_id",contents_list_style)]
        if not actions.user.element_match(actions.user.safe_focused_element(),prop_list):
            actions.user.key_to_matching_element("right",prop_list)
    def arc_pan(direction: str, screen_prop: float = 0.5):
        """Pans the map for duration expressed relative to the default duration 
        which is 0.5 seconds."""
        # start in the center of the map or layout
        prop_list = ["or",[("class_name","LayoutPaneView"),("class_name","MapPaneView")]]
        root = actions.user.window_root()
        print(f'root: {root}')
        prop_seq = [
            [("class_name","FrameworkDockSite")],
            [("class_name","DockHost")],
            [],
            [],
            [],
            [("class_name","Workspace")],
            [],
            [],
            [("class_name","DocumentWindow")],
            [("class_name",".*PaneView")]
        ]
        # el = actions.user.matching_element(prop_list,max_level = 10)
        el = actions.user.find_el_by_prop_seq(prop_seq,root)
        if el:
            x = el.rect.x + int(el.rect.width/2)
            y = el.rect.y + int(el.rect.height/2)
            ctrl.mouse_move(x,y)
            actions.sleep(0.02)
            # determine pixels from screen proportion
            dist_pixels = screen_prop * min(el.rect.width,el.rect.height)
            dx,dy = compass_diffs[direction]
            x += -1 * dx * dist_pixels
            y += -1 * dy * dist_pixels
            # drag
            actions.user.mouse_drag(0)
            actions.sleep(0.1)
            actions.user.slow_mouse(x,y,500)
            actions.sleep(0.6)
            actions.user.mouse_drag_end()

    def arc_create_custom_layout(wd: float, ht: float):
        """Creates a new layout with the given dimensions"""
        # open the menu command
        actions.user.arc_call_ribbon_item("Insert,Project,New Layout")
        # makes sure it is open
        prop_list = [("automation_id","esri_layouts_gallery")]
        el = actions.user.wait_for_element(prop_list)
        if el:
            state = actions.user.el_prop_val(el,'expand_collapse_state')
            print(f'state: {state}')
            it = 0
            while not state == "Expanded" and it < 5:
                actions.sleep(0.1)
                state = actions.user.el_prop_val(el,'expand_collapse_state')            
            if state == "Expanded":
                prop_list = [("name","Custom.*")]
                el = actions.user.key_to_matching_element("tab",prop_list,mod_func = remove_underscores)
                print(f'el: {el}')
                if el:
                    # invoke ribbon control to open custom layout dialog
                    actions.user.act_on_element(el,'invoke')
                    # make sure that the dialog is open
                    prop_list = [("class_name","ListBoxItem")]
                    el = actions.user.wait_for_element(prop_list)
                    print(f'el: {el}')
                    if el:
                        # tab over to the width text box
                        prop_list = [("name","Width")]
                        el = actions.user.key_to_matching_element("tab",prop_list,match_type = "ancestor")
                        print(f'el: {el}')
                        if el:
                            actions.key("ctrl-a")
                            actions.insert(f"{wd} in")
                            actions.key("tab ctrl-a")
                            actions.insert(f"{ht} in")
                            actions.user.arc_tab_to_button("OK",True)
                            # record for posterity
                            global layout_wd
                            global layout_ht
                            layout_wd = wd
                            layout_ht = ht
    def arc_draw_rectangle_on_layout():
        """Draws rectangle in center of layout, to be repositioned later"""
        print("we are here")
        root = actions.user.window_root()
        prop_seq = [
                    [("class_name","FrameworkDockSite")],
                    [("class_name","DockHost")],
                    [("class_name","SplitContainer")],
                    [("class_name","Workspace")],
                    [("class_name","TabbedMdiContainer")],
                    [("automation_id","esri_layouts.*"),("class_name","DockingWindowContainerTabItem")],
                    [("automation_id","esri_layouts.*"),("class_name","DocumentWindow")]
            ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        print(f'el: {el}')
        if el:
            x = el.rect.x + int(el.rect.width/3)
            y = el.rect.y + int(el.rect.height/3)
            actions.user.slow_mouse(x,y,300)
            actions.sleep(0.3)
            actions.user.mouse_drag(0)
            actions.sleep(0.05)
            x = el.rect.x + int(2*el.rect.width/3)
            y = el.rect.y + int(2*el.rect.height/3)        
            actions.user.slow_mouse(x,y,750)
            actions.sleep(0.76)
            actions.user.mouse_drag_end()
    def arc_expand_map_to_layout():
        """resizes current map frame to fill up layout"""
        # pull up X ribbon item
        global layout_wd
        global layout_ht
        if layout_wd == -1 or layout_ht == -1:
            print("unable to obtain layout width or height")
            return
        actions.user.arc_call_ribbon_item("Map Frame,Size & Position,Size & Position,a=X")
        el = actions.user.safe_focused_element()
        print(f'el: {el}')
        # makes sure we're there
        prop_list = [("automation_id","X")]
        el = actions.user.wait_for_element(prop_list)
        print(f'el: {el}')
        el = actions.user.safe_focused_element()
        print(f'el automation_id: {actions.user.el_prop_val(el,"automation_id")}')
        if el:
            actions.key("ctrl-a")
            actions.insert("0")
            actions.sleep(0.1)
            actions.key("tab ctrl-a")
            actions.insert("0")
            actions.sleep(0.1)
            actions.key("tab ctrl-a")
            actions.insert(f"{layout_wd}")
            actions.sleep(0.1)
            actions.key("tab ctrl-a")
            actions.insert(f"{layout_ht}")
            actions.sleep(0.1)
            actions.key("enter")

    def arc_scale_text():
        """Places focus on the scale text element"""
        print("FUNCTION arc_scale_text")
        actions.key("esc:5")
        root = actions.user.window_root()
        prop_seq = [
            [("class_name","FrameworkDockSite"),("automation_id","dockSite")],
            [("class_name","DockHost"),("automation_id","dockSite.PART_DockHost")],
            [("class_name","SplitContainer")],
            [("class_name","Workspace")],
            [("class_name","TabbedMdiContainer")],
            [("class_name","DockingWindowContainerTabItem")],
            [("class_name","DocumentWindow")],
            [("class_name",".*PaneView")],
            [("class_name",".*ReadoutControl"),("automation_id",".*ReadoutControl")],
            [("class_name","ScaleControl"),("automation_id","_scaleControl")],
            [("class_name","ExtendedComboBox"),("automation_id","_comboBox")],
            [("class_name","TextBox"),("automation_id","PART_EditableTextBox")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        print(f'el: {el}')
        actions.user.act_on_element(el,"click")
    def arc_nav_coord(coord: str = ""):
        """navigates to the given coordinates, expressed as '<easting>,<northing>'"""
        print(f'coord: {coord}')
        if coord != None:
            print("We are in!")
            if coord != '':
                x,y = [float(x) for x in coord.split(",")]            
            # see if control wrapper is already available
            root = actions.user.window_root()
            prop_seq = [
                [("class_name","AirspaceControlWrapper")],
                [("class_name","GotoXYView")],
            ]
            container = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
            if not container:
                # use keyboard shortcut
                actions.key("alt-t")
                container = actions.user.find_el_by_prop_seq(prop_seq,root)
            print(f'container: {container}')

            if container:
                prop_list = [("class_name","TextBox"),("help_text","Enter longitude.")]
                el = actions.user.matching_child(container,prop_list)
                print(f'el: {el}')
                if el:
                    actions.user.act_on_element(el,'select')
                    if coord == '':
                        return 
                    actions.key("ctrl-a")
                    actions.insert(str(x))
                    prop_list = [("class_name","TextBox"),("help_text","Enter latitude.")]
                    el = actions.user.matching_child(container,prop_list)
                    if el:
                        actions.user.act_on_element(el,'select')
                        actions.key("ctrl-a")
                        actions.insert(str(y))
                        prop_list = [("name","Specify the location unit format.")]
                        el = actions.user.matching_child(container,prop_list)
                        if el:
                            actions.user.act_on_element(el,'select')
                            actions.key("alt-down")
                            prop_list = [("name","Decimal Degrees")]
                            actions.key("up:7")
                            actions.user.key_to_matching_element("down", prop_list)
                            item = actions.user.wait_for_element(prop_list)
                            if item:
                                actions.key("enter")
                                prop_list = [("name","Pan the map to the provided location.")]
                                el = actions.user.matching_child(container,prop_list)
                                if el:
                                    actions.user.act_on_element(el,'invoke')
                                    # actions.sleep(1)
                                    actions.user.arc_call_ribbon_item("Map,Navigate,Go To XY")
                                    actions.key("esc")
                                    
    def arc_insert_text():
        """Selects a text insertion option from the insert menu"""
        # first navigate to the "Additional Surrounds" item just to the left of the text options
        actions.user.arc_call_ribbon_item("Insert,Map Surrounds,Additional Surrounds")
        # tab one more time to get element, entered open it up and tabbed to move to first option
        actions.key("tab enter tab")
    def arc_set_position(attr: str,val: float):
        """Sets the value of X,Y,Width or Height"""
        num_tabs = 0
        if attr == "Width":
            attr = "Y"
            num_tabs = 1
        if attr == "Height":
            attr = "Y"
            num_tabs = 2
        actions.user.arc_invoke_menu_item("esri_layouts_FormatTab",attr)
        for i in range(num_tabs):
            actions.key("tab")
        actions.key("ctrl-a")
        actions.insert(f"{float(val)}")
        actions.key("enter esc")
    def arc_select_map_in_contents():
        """Selects the map item in the table of contents"""
        # first check to see if a map is not already selected
        el = actions.user.safe_focused_element()
        prop_list = [("class_name","TreeViewItem"),("automation_id","mappingTOCItem_Map.*")]
        if not actions.user.element_match(el,prop_list):
            root = actions.user.window_root()
            prop_seq = [
                [("class_name","FrameworkDockSite")],
                [("class_name","DockHost")],
                [("class_name","SplitContainer")],
                [("class_name",".*ToolWindowContainer")],
                [("class_name",".*ToolWindow"),("name","Contents")],
                [("class_name","ContentsDockPane")],
                [("class_name","TOCControl")],
                [("class_name","TreeView")],
                [("class_name","TreeViewItem"),("automation_id","mappingTOCItem_Map.*")]
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
            actions.user.act_on_element(el,"select")
            actions.key("down up")
    def arc_map_coordinate_system():
        """Navigates to the map coordinate system"""
        print("FUNCTION arc_map_coordinate_system")
        actions.user.arc_select_map_in_contents()
        actions.user.arc_context_item("Properties")
        
        actions.key("enter")
        actions.sleep(0.2)
        el = ui.active_window().element
        prop_seq = [
                [("class_name","ListPropertySheet")],
                [("automation_id","PropertySheetListBox")],
                [("automation_id","esri_mapping_coordinateSystemPropertyPage")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq)
        actions.user.act_on_element(el,"select")
        prop_seq = [
                [("class_name","ListPropertySheet")],
                [("class_name","PageHost")],
                [("class_name","CoordinateSystemView")],
                [("automation_id","CoordinateSystemPickerControl")],
                [("automation_id","CSTree")],
                [("class_name","TreeViewItem")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq)
        actions.user.act_on_element(el,"select")
        for i in range(20):
            actions.key("down left")

    def arc_label_control(tab: str, group: str = ''):
        """Selects the given label control"""
    def arc_label_group(tab: str, group: str = ''):
        """Selects the given label group and returns the group element if successful"""

        # TOOL WINDOW
        tool_window = actions.user.arc_tool_window("Label Class.*")
        if tool_window:
            # UPPER TAB
            prop_seq = [
                [("class_name","LabelClassDockPane")],
                [("class_name","ListBox"),("automation_id","LabelingHeaderPane")],
                [("class_name","ListBoxItem"),("name",tab)]
            ]
            tab_el = actions.user.find_el_by_prop_seq(prop_seq,tool_window)
            if tab_el:
                # TAB GROUP
                actions.user.act_on_element(tab_el,'select')
                tab_el = actions.user.wait_for_element(prop_seq[-1],time_limit = 3)
                print(f'tab_el: {tab_el}')
                if tab_el:
                    if group != '':
                        prop_seq = [
                            [("class_name","LabelClassDockPane")],
                            [("class_name","TabControl")],
                            [("class_name","ListBox"),("automation_id",f".*{tab}.*PropertiesTabControl.*")],
                            [("class_name","ListBoxItem")]
                        ]
                        # el = actions.user.find_el_by_prop_seq(prop_seq,tool_window,verbose = True)
                        # print(f'el: {el}')
                        # children = actions.user.el_prop_val(el,'children')
                        # print(f'children: {children}')
                        # return 
                        if group.isnumeric():
                            ordinal = int(group)
                        else:
                            ordinal = 1
                            prop_seq[-1] = [("class_name","ListBoxItem"),("name",group)]
                        group_el = actions.user.find_el_by_prop_seq(prop_seq,tool_window,ordinal = ordinal,verbose = True)
                        print(f'group_el: {group_el}')
                        if group_el:
                            actions.user.act_on_element(group_el,'select')
                            group_el = actions.user.wait_for_element(prop_seq[-1])
                        else:
                            # above often comes up with an error, let's try keyboard shortcuts
                            print("group not found, trying keyboard shortcuts")
                            actions.key("tab")
                            prop_list = [("class_name","ListBoxItem")]
                            el = actions.user.wait_for_element(prop_list)
                            if el:
                                actions.key("left:3")
                                if group.isnumeric():
                                    actions.key(f"right:{group - 1}")
                                else:
                                    prop_list = prop_seq[-1]
                                    if not actions.user.element_match(el,prop_list):
                                        actions.user.key_to_matching_element("right",prop_list,limit = 3)

    def arc_nav_nth_symbol(n: int):
        """Attempts to navigate to and return the nth symbol in, for example, graduated symbols"""
        print("FUNCTION: arc_nav_nth_symbol")
        tool_window = actions.user.arc_tool_window("Symbology")
        if tool_window:
            prop_seq = [
                [("class_name","SymbologyDockPane")],
                [("class_name","TabControl")],
                [("class_name","TabItem"),("name","Classes")],
                [("class_name","EditSafeDataGrid")],
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,tool_window,verbose = True)
            if el:
                # look for group
                prop_list = [("class_name","GroupItem")]
                group_item = actions.user.matching_child(el,prop_list)
                if group_item:
                    el = group_item
                # get grid row
                prop_list = [("class_name","DataGridRow")]
                children = actions.user.matching_children(el,prop_list)
                print(f'children: {children}')
                if children:
                    if n <= len(children):
                        child = children[n - 1]
                        prop_seq = [
                            [("class_name","DataGridCell")],
                            [("class_name","Button")]
                        ]
                        el = actions.user.find_el_by_prop_seq(prop_seq,child,verbose = True)
                        if el:
                            print(f'el: {el}')
                            actions.user.act_on_element(el,"invoke")
                            actions.key("enter")
                            actions.user.arc_symbol_tab("properties")
       
    def arc_tab_to_parameter(prop_str: str):
        """tabs to the given parameter in a geoprocessing tool dialog"""
        # make sure that tool dialog is active
        el = actions.user.safe_focused_element()
        prop_list = ["or",
            [("class_name","ToolDialog.*"),("name","Geoprocessing")]
        ]
        tool_window = actions.user.matching_ancestor(el,prop_list)
        if tool_window:
            print("Successfully obtained tool dialog)")
            actions.user.mouse_to_obj_handle(el.rect,"top",100,y_offset=25)
            actions.sleep(0.2)
            # allow simple names instead of property strings
            if not "=" in prop_str:
                prop_str = f"n={prop_str}"
            prop_list = actions.user.get_property_list(prop_str)
            actions.user.key_to_matching_element(
                "tab",
                prop_list,
                delay = 0.03,
                avoid_cycles = True)
            # shouldn't hurt to press alt-down
            actions.key("alt-down")
        else:
            print(f"Unable to obtain tool dialog ({el})")
    def arc_drag_list_item(up_or_down: str):
        """sets up compass to drag item in a list"""
        el = actions.user.safe_focused_element()
        if el:
            rect = el.rect
            if rect:
                x = int(el.rect.left + el.rect.width/2)
                y = int(el.rect.top + 2)
                ctrl.mouse_move(x,y)
                if up_or_down.lower() == "up":
                    actions.user.compass_enable(0)
                else:
                    actions.user.compass_enable(180)
    def arc_show_records(option: str = "Selected"):
        """shows selected records in is currently focused attribute table"""
        # navigate upward to docking window container tab item
        el = actions.user.safe_focused_element()
        print(f'el: {el}')
        if el:
            prop_list = [("class_name","DockingWindowContainerTabItem")]
            container = actions.user.matching_ancestor(el,prop_list)
            print(f'container: {container}')
            if container:
                prop_seq = [
                    [("class_name","DocumentWindow")],
                    [("class_name","TableCorePaneView")],
                    [("class_name","TablePaneControl")],
                    [("class_name","TableCoreControl")],
                    [("class_name","TableNavigationControl")],
                    [("name",f"Show {option} Records")]
                ]
                el = actions.user.find_el_by_prop_seq(prop_seq,container,verbose = True)
                print(f'el: {el}')
                if el:
                    actions.user.act_on_element(el,"toggle")

    def arc_run_tool(tool_name: str = ''):
        """runs the specified geoprocessing tool"""
        # make sure the geoprocessing tool panel is open
        actions.user.arc_call_ribbon_item("Analysis,Geoprocessing,Tools")
        # this always seems to land us in the search panel;
        # if there are exceptions to this well need to change later
        
        # access the tool search textbox
        root = actions.user.window_root()
        prop_seq = [
        	[("class_name","FrameworkDockSite")],
        	[("class_name","DockHost")],
            # we have a problem here: sometimes we need to dig down into one split container,
            # sometimes two
        	[("class_name","SplitContainer")],
        	[("class_name","SplitContainer")],
        	[("class_name",".*ToolWindowContainer")],
        	[("name","Geoprocessing"),("class_name","DockingWindowContainerTabItem")],
        	[("name","Geoprocessing"),("class_name",".*ToolWindow")],
        	[("class_name","GPDocPaneView")],
        	[("name","Search"),("class_name","TextBox")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        if el:
            # set the value to the tool name
            print(f'el: {el}')
            actions.user.set_el_prop_val(el,"value",tool_name)
            if tool_name != '':
                actions.sleep(1)
                actions.key("tab:4 down up")
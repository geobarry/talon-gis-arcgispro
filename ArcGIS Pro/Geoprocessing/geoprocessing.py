# OBSERVATIONS/ASSUMPTIONS
# 1. Elements do not reliably have names. 
# 2. The element structure is flat. Everything is a child of the same "Custom" element (returned by get_parameter_container())
# 3. Every parameter has an element with a name that shows up as text. 
# 4. These are either control_type 'text' or 'checkbox' (look out for other possibilities)
# 5. Other control parameters all appear after the corresponding text element, except...
# 6. The help button appears immediately before the text element, but is ephemeral...
# 7. ...so the only reliable way to get to it is to first select the first real control element and then press shift-tab

from talon import Module, Context, actions

mod=Module()

mod.list("arc_gp_dynamic_parameter","name of parameter in current geoprocessing tool dialog")

def geoprocessing_panel():
    """returns the object with name='Geoprocessing',control_type='Pane'"""
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
    ]
    el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
    # if nothing is found we probably need to open the panel
    if not el:
        actions.user.arc_call_ribbon_item("Analysis,Geoprocessing,Tools")        
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
    return el
def get_parameter_container():
    """retrieves custom element that contains all of the parameters"""
    panel=geoprocessing_panel()
    if panel:
        prop_seq=[
            [("automation_id","gp_doc_pane")],
            [("automation_id","gp_tool_dialog")],
            [("class_name","ScrollViewer")],
            [("control_type","Custom")]
        ]
        container=actions.user.find_el_by_prop_seq(prop_seq,panel,verbose=False)
        return container


param_dict={}
def fetch_parameters():
    """retrieves list of parameter names for dynamic list and simultaneously saves control list and dictionary of (text controls) and corresponding ids to global variables"""
    container=get_parameter_container()
    if container:
        param_dict.clear()
        param_ctrl_list=actions.user.el_prop_val(container,'children')
        if param_ctrl_list:
            name_list=[]
            param_name=None
            for control in param_ctrl_list:
                control_type=actions.user.el_prop_val(control,'control_type')
                if control_type.lower() in ['text','checkbox']:
                    param_name=actions.user.el_prop_val(control,'name')
                    param_dict[param_name] = []
                    name_list.append(param_name)
                if param_name and control_type.lower() not in ['text','image']:
                    param_dict[param_name].append(control)
            return name_list

ctx=Context()

@ctx.dynamic_list("user.arc_gp_dynamic_parameter")
def arc_gp_dynamic_parameter(_) -> dict[str,str]:
    name_list=fetch_parameters()
    if name_list:
        out = actions.user.create_spoken_forms_from_list(name_list)
        return out
        
@mod.action_class
class Actions:
    def arc_run_tool(tool_name: str = ''):
        """runs the specified geoprocessing tool"""
        # obtain the geoprocessing panel
        panel = geoprocessing_panel()
        if not panel:
            return
        # access the tool search textbox
        prop_seq = [
            [("class_name","GPDocPaneView")],
            [("name","Search"),("class_name","TextBox")]
        ]
        search_box = actions.user.find_el_by_prop_seq(prop_seq,panel,verbose = True)
        if search_box:
            # set the value to the tool name
            actions.user.set_el_prop_val(search_box,"value",tool_name)
            if tool_name != '':
                prop_seq=[
                    [("class_name","GPDocPaneView")],                    
                    [("class_name","SearchToolsView")],
                    [("class_name","ListView")]
                ]
                container=actions.user.find_el_by_prop_seq(prop_seq,panel)
                if container:
                    prop_list=[("name",tool_name)]
                    tool_el=actions.user.matching_child(container,prop_list)
                    if tool_el:
                        actions.sleep(1)
                        actions.key('down')
                        el=actions.user.wait_for_element(prop_list)
                        if el:
                            actions.user.act_on_focused_element("click")
    def arc_select_parameter(param_name: str, kw: str = 'select'):
        """Selects a given parameter with an a geoprocessing tool; param_name must be arc_gp_dynamic_parameter to avoid stale elements"""
        el_list=param_dict[param_name]
        print(f'el_list: {el_list}')
        # default to first element
        trg_ctrl=el_list[0]
        # determine actual element based on keyword
        match kw:
            case 'select':
                # priority order if property string is not designated
                if len(el_list) > 1:
                    priority_list=[
                        [("control_type","CheckBox")],
                        [("control_type","Edit")],
                        [("control_type","ComboBox")]
                    ]
                    def get_priority_level(control):
                        for idx,prop_list in enumerate(priority_list):
                            if actions.user.element_match(control,prop_list):
                                return idx
                        return len(priority_list)
                    priority_min=get_priority_level(trg_ctrl)
                    for control in el_list[1:]:
                        priority=get_priority_level(control)
                        if priority < priority_min:
                            priority_min=priority
                            trg_ctrl=control
            case 'browse':
                prop_list=[("help_text","Browse")]
                trg_ctrl=next((control for control in el_list if actions.user.element_match(control,prop_list)),None)
            case 'expand':
                prop_list=[("control_type","ComboBox")]
                trg_ctrl=next((control for control in el_list if actions.user.element_match(control,prop_list)),None)                
            case 'toggle':
                prop_list=[("control_type","Checkbox")]
                trg_ctrl=next((control for control in el_list if actions.user.element_match(control,prop_list)),None)                
        print(f'trg_ctrl: {trg_ctrl}')
        # take action on target control
        if trg_ctrl:
            match kw:
                case 'select':
                    actions.user.act_on_element(trg_ctrl,'select')
                case 'browse':
                    actions.user.act_on_element(trg_ctrl,'invoke')
                case 'expand':
                    actions.user.act_on_element(trg_ctrl,'expand')
                case 'toggle':
                    actions.user.act_on_element(trg_ctrl,'toggle')
    
    
    
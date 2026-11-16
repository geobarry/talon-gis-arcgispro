from talon import Module, actions, clip

mod=Module()

def set_folder(folder_name: str):
    """sets the folder in the address bar"""
    root = actions.user.window_root()
    prop_seq = [
        [("automation_id","_breadCrumb")]
    ]
    el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
    actions.user.set_el_prop_val(el,"value",folder_name)

def focus_content_panel():
    """places focus on the catalogList content panel"""
    root = actions.user.window_root()
    prop_seq = [
        [("automation_id","catalogList")],
    ]
    container = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
    if container:
        item_sel_list=actions.user.el_prop_val(container,'selection')
        print(f'len(item_sel_list): {len(item_sel_list)}')
        if len(item_sel_list) > 0:
            item_sel=item_sel_list[0]
            actions.user.act_on_element(item_sel,'select')
        else:
            prop_list=[("control_type","DataItem")]
            item_list=actions.user.matching_children(container,prop_list)
            if item_list and len(item_list) > 0:
                item=item_list[0]
                actions.user.act_on_element(item,'select')

@mod.action_class
class Actions:
    def arc_browse_set_folder(folder_name: str = ""):
        """Navigates to the input folder in the ArcGIS Pro browse dialog"""
        if not folder_name:
            # get folder named from clipboard
            folder_name=clip.text()
        print(f'folder_name: {folder_name}')
        set_folder(folder_name)
        focus_content_panel()
    
    def arc_browse_focus_content():
        """places focus on the catalogList"""
        focus_content_panel()
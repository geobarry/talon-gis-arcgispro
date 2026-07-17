from talon import Module, Context, actions

mod=Module()

mod.list("arc_dynamic_project", "Projects listed on start screen")

ctx=Context()

def project_list():
    """Returns list element whose children represent individual projects"""
    root = actions.user.window_root()
    prop_seq = [
        [("class_name","StartPage")],
        [("class_name","ScrollViewer")],
        [("class_name","StartPageHomeContent")],
        [("class_name","RecentProjectsListControl")],
        [("class_name","ListBox")],
    ]
    el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
    return el
    
def act_on_project(prj_el, action):
    if prj_el:
        actions.user.act_on_element(prj_el,'select')
        if action == "open" or action == "invoke":
            actions.user.act_on_element(prj_el,'click')
global prj_dict
prj_dict={}

@ctx.dynamic_list("user.arc_dynamic_project")
def arc_dynamic_project(_) -> dict[str,str]:
    """names for projects in start screen"""
    container=project_list()
    prop_list=[("class_name","ListBoxItem")]
    children=actions.user.matching_children(container,prop_list)
    if children:
        name_list=[(actions.user.el_prop_val(child,'name'), child) for child in children]
        global prj_dict
        spoken_form_dict,prj_dict = actions.user.create_spoken_form_mappings(name_list)
        return spoken_form_dict
        
@mod.action_class
class Actions:
    def arc_act_on_project(prj_key: str, action: str = "select", ordinal: int = 1):
        """selects or opens the given project"""
        prj_list=prj_dict[prj_key]
        if prj_list and len(prj_list) >= ordinal:
            act_on_project(prj_list[ordinal - 1], action)
            
    def arc_act_on_project_by_id(id: int = 1,action: str = "select"):
        """Performs action on the given project element"""
        container=project_list()
        prop_list=[("class_name","ListBoxItem")]
        children=actions.user.matching_children(container,prop_list)
        if children and len(children) >= id:
            el=children[id - 1]
            act_on_project(el, action)

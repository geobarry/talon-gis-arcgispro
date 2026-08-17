from talon import Module, actions

mod=Module()

@mod.action_class
class Actions:
    def arc_backstage_tab(name: str):
        """Selects the given tab on the left in the backstage in ArcGIS Pro"""
        root = actions.user.window_root()
        prop_seq = [
        	[("automation_id","backStageTabControl")],
        	[("name",name)]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        actions.user.act_on_element(el,'select')
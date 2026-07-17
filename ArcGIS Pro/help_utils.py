from talon import Module, actions
import os

mod=Module()

def base_folder():
    """obtains the path to the base folder within the user's talent directory"""
    folder_cur=os.path.dirname(os.path.abspath(__file__))
    return folder_cur

def get_module_id(rel_path):
    base=base_folder()
    item_list=base.split("\\")
    item_list=item_list[item_list.index("user"):]
    item_list += rel_path.split(".")
    if item_list[-1] != "talon":
        item_list += ["talon"]
    mod_id=".".join(item_list)
    return mod_id
        
@mod.action_class
class arc_help_utils_Actions:
    def arc_help_module(rel_path: str):
        """brings up help imgui for given module"""
        mod_id=get_module_id(rel_path)
        actions.user.help_search_context(mod_id)

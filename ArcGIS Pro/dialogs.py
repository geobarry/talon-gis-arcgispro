from talon import Context,Module,actions

mod=Module()

@mod.action_class
class Actions:
    def arc_dialog_button(button_name: str, action: str = None):
        """Attempts to locate the given button just under the dialog window using uiautomation"""
        root=actions.user.window_root()
        print(f'root: {root}')
        if root:
            prop_list=[("name",button_name),("class_name","Button")]
            button=actions.user.matching_child(root,prop_list)
            if button:
                if action:
                    actions.user.act_on_element(button,action)
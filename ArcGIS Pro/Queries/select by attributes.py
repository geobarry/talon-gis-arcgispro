from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax
import re, time

mod = Module()

@mod.action_class
class Actions:
    def arc_quick_select_by_attributes(field_name: str, val: str|int|float, predicate: str = "is equal to"):
        """quickly selects within the currently selected layer"""
        print("attempting selection...")
        # select by attributes
        actions.key("esc:5 alt-m s b a")
        root=actions.user.wait_for_matching_ancestor([("automation_id","gp_tool_dialog.*")])
        print(f'root: {root}')
        if root:
            # go to field ComboBox
            actions.user.arc_select_nth_clause_item(1,"field")
            # enter field name
            actions.insert(field_name)
            # go to predicate ComboBox
            actions.user.arc_select_nth_clause_item(1,"predicate")
            actions.insert(predicate)
            # go to value ComboBox, open it for autocomplete functionality
            actions.user.arc_select_nth_clause_item(1,"value")
            actions.key("alt-down")
            actions.sleep(0.5)
            actions.insert(val)

    def arc_quick_assign_value(field_name: str, val: str|int|float):
        """quickly assigns value to selected features in open attribute table using Calculate Field"""
        # open calculate field dialog 
        actions.user.slow_key_press("esc:5 alt t v t c")
        root=actions.user.wait_for_matching_ancestor([("automation_id","gp_tool_dialog.*")])
        print(f'root: {root}')
        if root:
            # go to field name combo box
            prop_seq = [
#                [("class_name","ToolDialogPage"),("automation_id","gp_tool_dialog")],
                [("class_name","ScrollViewer")],
                [("control_type","Custom")],
                [("class_name","ComboBox"),("automation_id","fields_combo")]
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
            if el:
                # navigate to and select expression editor
                actions.user.set_el_prop_val(el,"value",field_name)
                prop_seq = [
                    [("automation_id","gp_tool_dialog")],
#                    [("class_name","ScrollViewer")],
                    [("control_type","Custom")],
                    [("automation_id","expressionBuilderControlRoot")],
                    [("name","textExpressionEditor"),("automation_id","textExpressionEditor")],
                    [("name","Editor View"),("automation_id","EditorViewDefault")]
                ]
                el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
                print(f'el: {el}')
                print(f'el text: {actions.user.el_prop_val(el,"text")}')
                print(f'el value: {actions.user.el_prop_val(el,"value")}')
                if el:
                    actions.user.act_on_element(el,'select')
                    # insert value
                    actions.key("ctrl-a")
                    # we are going to assume the value is a number if it is numeric
                    val=str(val)
                    if not val.isnumeric():
                        val=f"'{val}'"
                    actions.insert(str(val))
                    # select ok button (don't invoke because this is sensitive?)
                    prop_list=[("automation_id","Ok_btn")]
                    el=actions.user.matching_child(root,prop_list)
                    if el:
                        actions.user.act_on_element(el,'select')
                    
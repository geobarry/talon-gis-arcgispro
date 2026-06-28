from talon import actions, Module, Context

mod=Module()

el_dict={
    "Input Table":"ct=ComboBox;n=Input Table.*,c=TextBox",
    "Field Name":"a=fields_combo",
    "Expression Type":"ct=ComboBox;n=Expression Type.*,c=Textbox",
    "Fields":"a=expressionBuilderControlRoot;a=SelectedFieldListBox",
    "Helpers":"a=expressionBuilderControlRoot;a=ExpressionFunctionsListBox",
    "Expression":"c=TextExpressionBuilderView;n=textExpressionEditor",
    "Code Block":"c=TextExpressionBuilderView;n=textCodeBlockEditor"
}

"""returns the element with control_type=Custom that contains all of the parameters"""
def get_main_panel():
    root=actions.user.window_root()
    if root:
        prop_seq=[
            [("class_name","ToolDialogPage")],
            [("class_name","ScrollViewer")],
            [("control_type","Custom")]
        ]
        el=actions.user.find_el_by_prop_seq(prop_seq,root)
        return el

@mod.action_class
class Actions:
    def arc_calc_field_select(control_name: str):
        """selects the given control in the calculate field dialog"""
        root=get_main_panel()
        if root:
            prop_seq_str=el_dict[control_name]
            prop_seq=actions.user.get_property_sequence(prop_seq_str)
            if prop_seq:
                el=actions.user.find_el_by_prop_seq(prop_seq,root,verbose=True)
                if el:
                    actions.user.act_on_element(el,'select')
                return el
		
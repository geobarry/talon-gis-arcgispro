from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax, ui as winui

mod = Module()

@mod.action_class

class Actions:
    def arc_definition_query_list():
        """Return the list box containing all of the queries"""
        root = actions.user.window_root()
        if root:
            # Definition Query
            root = actions.user.window_root()
            prop_seq = [
                [("class_name","ListPropertySheet")],
                [("class_name","PageHost")],
                [("class_name","DefinitionQueryView")],
                [("class_name","MultipleDefinitionQueryView")],
                [("class_name","ListBox"),("automation_id","listbox")],
            ]
            el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
            return el
    def arc_selected_definition_query():
        """returns the selected definition query item from the query list"""
        query_list = actions.user.arc_definition_query_list()
        if query_list:
            selection = actions.user.el_prop_val(query_list,'selection')
            print(f'selection: {selection}')
            if selection:
                if len(selection) > 0:
                    selection = selection[0]
                    return selection
            # if nothing selected, select first query
            children=actions.user.el_prop_val(query_list,'children')
            print(f'len(children): {len(children)}')
            if children:
                if len(children) > 0:
                    return children[0]
    def query_select_nth(ordinal: int):
        """selects the nth query"""
        query_list = actions.user.arc_definition_query_list()
        if query_list:
            children = actions.user.el_prop_val(query_list,'children')
            if children:
                if len(children) >= ordinal:
                    query = children[ordinal - 1]
                    if query:
                        actions.user.act_on_element(query,'select')
    def query_toggle_sql():
        """Toggles the SQL button"""
        query = actions.user.arc_selected_definition_query()
        if query:
            prop_seq = [
                [("class_name","DefinitionQueryItemView")],
                [("automation_id","queryBuilderControlRoot")],
                [("automation_id","advancedMode")]
            ]
            check_box = actions.user.find_el_by_prop_seq(prop_seq,query,verbose = True)
            actions.user.act_on_element(check_box,'select')
            el = actions.user.wait_for_element(prop_seq[-1])
            if el:
                actions.key("space")

    def query_activate_selected():
        """Activates the selected query"""
        query = actions.user.arc_selected_definition_query()
        prop_seq = [
            [("class_name","DefinitionQueryItemView")],
            [("automation_id","setActiveQueryButton")]
        ]
        button = actions.user.find_el_by_prop_seq(prop_seq,query)
        if button:
            actions.user.act_on_element(button,'invoke')
    def query_rename_selected(name: str = ""):
        """Renames the selected query"""
        query = actions.user.arc_selected_definition_query()
        prop_seq = [
            [("class_name","DefinitionQueryItemView")],
            [("automation_id","queryBuilderControlRoot")],
            [("automation_id","queryNameTextBlock.*")]
        ]        
        txt_box = actions.user.find_el_by_prop_seq(prop_seq,query)
        if txt_box:
            if name == '':
                actions.user.act_on_element(txt_box,'select')
            else:
                actions.user.set_el_prop_val(txt_box,"value",name)
    def query_remove_item(name: str):
        """Remove item with given value"""
        prop_list = [("value",name)]
        actions.user.key_to_matching_element("tab",prop_list)
        el=actions.user.wait_for_element(prop_list)
        if el:
            actions.sleep(0.2)
            actions.key("tab enter")
    def query_include_multiple(field_name: str,val_list: list,append: bool = False):
        """Constructs scul query including multiple values"""
        print(f'val_list: {val_list}')
        val_list = [f"{field_name} = '{x}'" for x in val_list]
        clause = f" or ".join(val_list)
        if append:
            clause=f" or {clause}"
        print(f'clause: {clause}')
        actions.insert(clause)
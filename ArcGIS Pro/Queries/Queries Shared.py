from talon import Context,Module,actions
from talon.windows import ax as ax
import time

clause_item_dict = {
                'operator':"editingBooleanOperatorCombo",
                'field':"fieldNameComboBox",
                'predicate':"predicateListColumn",
                'value':"editingValueCombo",
                'remove button':"_deleteClauseButton"
            }

mod = Module()

mod.list("arc_selection_predicate","comparison operators used in selection")
mod.list("arc_clause_component","component of definition query or select by attributes or similar clause")
mod.list("conjunction","and/or")
mod.list("dynamic_query_clause","query clause selected by value")

ctx=Context()

ctx.lists["user.conjunction"] = ["and","or"]
ctx.lists["user.arc_clause_component"] = ["operator","field","predicate","value","remove button"]

def select_by_attributes_query_control():
    root = actions.user.window_root()
    if root:
        # Select by Attributes
        prop_seq = [
            [("class_name","ToolDialogPage"),("automation_id","gp_tool_dialog")],
            [("class_name","ScrollViewer")],
            [],
            [("automation_id","queryBuilderControlRoot")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
        return el
def definition_query_query_control():
    selection = actions.user.arc_selected_definition_query()
    print(f'selection: {selection}')
    if selection:
        prop_seq = [
            [("class_name","DefinitionQueryItemView")],
            [("class_name","QueryBuilderControlInternal"),("automation_id","queryBuilderControlRoot")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,selection)
        return el
def label_class_query_control():
    root = actions.user.window_root()
    prop_seq = [
        [("class_name","FrameworkDockSite")],
        [("class_name","DockHost")],
        [("class_name","SplitContainer")],
        [("class_name","SplitContainer")],
        [("class_name","ToolWindowContainer")],
        [("automation_id","esri_mapping_labelClassDockPaneTab")],
        [("automation_id","esri_mapping_labelClassDockPane")],
        [("class_name","LabelClassDockPane")],
        [("class_name","TabControl")],
        [("automation_id","LabelClassPageTabControl")],
        [("automation_id","queryBuilderControlRoot")],
    ]
    el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
    return el

clause_prop_list = [("name","ArcGIS.Desktop.Internal.Mapping.Controls.QueryBuilder.QueryBuilderExpressionClauseViewModel")]
comp_id_dict={
    'operator':"editingBooleanOperatorCombo",
    'field':"fieldNameComboBox",
    'predicate':"predicateListColumn",
    'value':"editingValueCombo",
    'remove button':"_deleteClauseButton"
}

def get_clause_comp(clause: ax.Element,comp_name: str = "value"):
    """returns the element of the clause"""
    if clause:
        prop_list=[("automation_id",comp_id_dict[comp_name])]
        children=actions.user.el_prop_val(clause,'children')
        return actions.user.matching_child(clause,prop_list)

def get_clause_by_value(trg_val: str):
    """returns the clause element"""
    query_box = actions.user.arc_query_box()
    r={}
    if query_box:
        clause_list = actions.user.matching_children(query_box,clause_prop_list)
        for clause in clause_list:
            el=get_clause_comp(clause,"value")
            val=actions.user.el_prop_val(el,'value')
            if val == trg_val:
                return clause
            
@ctx.dynamic_list("user.dynamic_query_clause")
def dynamic_query_clause(_) -> dict[str,str]:
    """Returns the value of the clause element"""
    
    query_box = actions.user.arc_query_box()
    r={}
    if query_box:
        clause_list = actions.user.matching_children(query_box,clause_prop_list)
        for clause in clause_list:
            el=get_clause_comp(clause,"value")
            if el:
                val=actions.user.el_prop_val(el,'value')
            r[val] = val
        return r
        
@mod.action_class
class Actions:
    def arc_selected_query():
        """returns the QueryBuilderControlInternal object"""
        # first look in ancestors
        el=actions.user.safe_focused_element()
        query_ctrl=actions.user.matching_ancestor(el,[("automation_id","queryBuilderControlRoot")])
        print(f'query_ctrl: {query_ctrl}')
        if query_ctrl:
            return query_ctrl
        el=select_by_attributes_query_control()
        if el:
            return el
        else:
            el=definition_query_query_control()
            print(f'el: {el}')
            if el:
                return el
            else:
                el=label_class_query_control()
                return el
    def arc_query_box():
        """returns the ListBox object"""
        query_builder = actions.user.arc_selected_query()
        print(f'query_builder: {query_builder}')
        if query_builder:
            prop_list = [("class_name","ListBox"),("automation_id","clausesListBox")]
            query_box = actions.user.matching_child(query_builder,prop_list)
            return query_box
    def arc_act_on_clause(val: str,comp: str = '',action: str = "select"):
        """Selects the given clause component, which should be captured by dynamic_query_clause"""
        clause=get_clause_by_value(val)
        if comp == '':
            actions.user.act_on_element(clause,action)
        else:
            comp=get_clause_comp(clause,comp)
            # delay actions other than select for visual feedback
            if action == "select":
                actions.user.act_on_element(comp,action)
            else:
                actions.user.act_on_element(comp,'select')
                actions.sleep(0.5)
                actions.user.act_on_element(comp,action)
    def arc_act_on_clauses(val_list: list,comp: str = '',action: str = "select"):
        """acts on multiple clauses at once"""
        print(f'val_list: {val_list}')
        for val in val_list:
            actions.user.arc_act_on_clause(val,comp,action)
        
    def arc_selected_clause():
        """returns the element with automation_id == clausesListBox"""
        # timing tests show that this is about 20% faster by going up the tree rather than down
        clause = actions.user.safe_focused_element()
        if clause:
            prop_list = [("name","ArcGIS\.Desktop\.Internal\.Mapping\.Controls\.QueryBuilder\.QueryBuilderExpressionClauseViewModel")]
            if not actions.user.element_match(clause,prop_list):
                clause = actions.user.matching_ancestor(clause,prop_list)
        return clause
    def arc_populate_selected_clause(conjunction: str = '', field: str = '', predicate: str = '', val: str = ''):
        """Populates the currently selected clause"""
        clause = actions.user.arc_selected_clause()
        print(f'clause: {clause}')
        if clause:
            actions.user.arc_populate_clause(clause,conjunction,field,predicate,val)
    def arc_populate_clause(clause: ax.Element, conjunction: str = '', field: str = '', predicate: str = '', val: str = ''):
        """Populates the input clause element, leaving the value combo box open"""
        if clause:
            actions.user.act_on_element(clause,'select')
            id_list=['operator','field','predicate','value']
            id_list=[comp_id_dict[id] for id in id_list]
            val_list = [conjunction,field,predicate,val]
            # In case of where clause, ignore conjunction
            if conjunction == "Where":
                id_list=id_list[1:]
                val_list=val_list[1:]
            for automation_id,val in zip(id_list,val_list):
                el = actions.user.safe_focused_element()
                prop_list = [("automation_id",automation_id)]
                el = actions.user.matching_child(clause,prop_list)
                print(f'automation_id: {automation_id} el: {el}')
                if el:                    
                    if automation_id == "PART_EditableTextBox":
                        actions.user.act_on_element(el,'select')
                        actions.key("alt-down")
                        if val != '':
                            actions.insert(val)
                    else:
                        actions.user.act_on_element(el,'select')
                        if val != '':
                            actions.insert(val)
                            actions.sleep(0.1)
    def arc_populate_new_clause(conjunction: str = '', field: str = '', predicate: str = '', val: str = ''):
        """Adds a new clause and populates it at the same time"""
        # add new clause
        actions.user.arc_query_add_clause()
        # select last clause
        actions.user.arc_select_nth_clause_item(-1)
        # fill in values
        actions.user.arc_populate_selected_clause(conjunction,field,predicate,val)
    def arc_query_add_multiple(conjunction: str,field: str,predicate: str,val_str_list: str):
        """Uses uiautomation to add multiple or clauses"""
        print(f'val_str_list: {val_str_list}')
        val_list=val_str_list.split(",")
        for val in val_list:
            actions.sleep(0.2)
            actions.user.arc_populate_new_clause(conjunction,field,predicate,val)
    def arc_nth_query_clause(n: int = 1):
        """returns the ListBoxItem object"""
        query_box = actions.user.arc_query_box()
        print(f'query_box: {query_box}')
        if query_box:
            children = actions.user.matching_children(query_box,clause_prop_list)
            if children:
                if -len(children) <= n <= len(children):
                    r = children[n - 1] if n > 0 else children[n]
                    return r
    def arc_select_nth_clause_item(n: int = 1,item_type: str = "clause",action: str = ''):
        """selects the nth clause, field, predicate, value or remove button"""
        ex = actions.user.arc_nth_query_clause(n)
        if item_type == 'clause':
            actions.user.act_on_element(ex,'select')
            return 
        elif ex:
            global clause_item_dict
            item_id = clause_item_dict[item_type]
            if item_id:
                prop_list = [("automation_id",item_id)]
                el = actions.user.matching_child(ex,prop_list)
                if el:
                    print(f'el: {el}')
                    actions.user.act_on_element(el,'select')
                    if action != '':
                        actions.user.act_on_element(el,action)
    def arc_query_remove_all():
        """Removes all clauses from current query"""
        query_box = actions.user.arc_query_box()
        if query_box:
            clause_list = actions.user.matching_children(query_box,clause_prop_list)
            n=len(clause_list)
            for idx in range(n):
                actions.user.arc_select_nth_clause_item(-1,'remove button','invoke')
    def arc_query_add_clause():
        """Adds a new clause and selects the clause element"""
        query_builder = actions.user.arc_selected_query()
        prop_list = [("automation_id","AddClauseButton")]
        button = actions.user.matching_child(query_builder,prop_list)
        if button:
            actions.user.act_on_element(button,'invoke')
            el = actions.user.wait_for_element(prop_list)
            print(f'AFTER PRESSING ADD CLAWS BUTTON el: {el}')
            if el:
                actions.user.arc_select_nth_clause_item(-1)
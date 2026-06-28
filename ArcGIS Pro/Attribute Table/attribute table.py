from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax, ui as winui

mod = Module()

def get_table_tab():
    """returns the element with esri_editing_table.*"""
    prop_list=[("automation_id","esri_editing_table.*")]
    el=actions.user.safe_focused_element()
    if el:
        if actions.user.element_match(el,prop_list):
            return el
        else:
            el=actions.user.matching_ancestor(el,prop_list)
            return el

@mod.action_class
class Actions:
    def arc_attribute_table_feature_command(keyboard_shortcut: str):
        """Flashes current feature"""
        # get document window containing table
        el = winui.focused_element()
        prop_list = [("automation_id","_tableDataGrid")]
        if actions.user.element_match(el,prop_list):
            print("we have a table grid!!!")
            prop_list = [("class_name","DocumentWindow")]
            el = actions.user.matching_ancestor(el,prop_list)
            if el:
                # save for later so we can get back to the panel
                panel_name = el.name
                print("we have a table name!!!")
                # make sure we have a table
                prop_list = [("class_name","TableCorePaneView")]
                t = actions.user.matching_child(el,prop_list)
                if t:
                    # use keyboard shortcut to flash feature
                    actions.key(keyboard_shortcut)
                    # get back to the table panel
                    actions.user.arc_select_panel(panel_name)
                    # seems that the left key will get you to the table itself
                    actions.key("left")
    def arc_fields_view_focus_new_field():
        """Sets the focus on the last field in field's view, i.e. the new field to be created"""
        root = actions.user.window_root()
        prop_seq = [
        	[("class_name","FrameworkDockSite"),("automation_id","dockSite")],
        	[("class_name","DockHost"),("automation_id","dockSite.PART_DockHost")],
        	[("class_name","SplitContainer")],
        	[("class_name","SplitContainer")],
        	[("class_name","Workspace")],
        	[("class_name","SplitContainer")],
        	[("class_name","TabbedMdiContainer")],
        	[("class_name","DockingWindowContainerTabItem"),("automation_id","esri_mapping_fieldsPane_.*Tab")],
        	[("class_name","DocumentWindow"),("automation_id","esri_mapping_fieldsPane_.*")],
        	[("class_name","FieldsPaneView")],
        	[("class_name","ThemedDataGrid"),("automation_id","FieldsViewDataGrid")],
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        print(f'el: {el}')
        if el:
            prop_list=[("class_name","DataGridRow")]
            item_list=actions.user.matching_children(el,prop_list)
            print(f'len(item_list): {len(item_list)}')
            if item_list and len(item_list) > 0:
                item=item_list[-2]
                prop_list=[("class_name","DataGridCell")] 
                cell_list=actions.user.matching_children(item,prop_list)
                print(f'len(cell_list): {len(cell_list)}')

                if cell_list:
                    cell=cell_list[2]
                    print(f'cell: {cell}')
                    actions.user.act_on_element(cell,'select')
    def arc_focus_table():
        """places the focus on the a selected row in the actual table within the table tab"""
        container=get_table_tab()
        print(f'container: {container}')
        if container:
            prop_seq=[
                [("class_name","TableCorePaneView")],
                [("class_name","TablePaneControl")],
                [("class_name","TableCoreControl")],
                [("automation_id","_tableDataGrid")]
            ]
            el=actions.user.find_el_by_prop_seq(prop_seq,container)
            print(f'el: {el}')
            if el:
                actions.user.act_on_element(el,'select')
        
    
ctx = Context()
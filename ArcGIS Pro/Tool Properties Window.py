from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax, ui as winui

mod = Module()
mod.list("arc_tool_properties_parameter_column","column in the parameter definition grid")



@mod.action_class
class Actions:
    def arc_tool_properties_select_row(row_label: str):
        """Select a given row according to its row label"""
        # See if we are in a grid cell, and if so get the column number
        col = 0
        el = winui.focused_element()
        if el:
            prop_list = [("class_name","DataGridCell")]
            cell = actions.user.matching_ancestor(el,prop_list)
            if cell:
                col = int(cell.name[-1])
        # obtain grid
        root = winui.active_window().element
        if root:
            prop_seq = [
                [("class_name","ListPropertySheet")],
                [("class_name","PageHost")],
                [("class_name","ToolParametersView")],
                [("class_name","EditSafeDataGrid")]
            ]
            grid = actions.user.find_el_by_prop_seq(prop_seq,root)
            prop_list = [("class_name","DataGridRow")]
            rows = actions.user.matching_children(grid,prop_list)
            prop_list = [("class_name","DataGridCell"),("name",f".*0"),]
            output_row = None
            for row in rows:
                prop_seq = [
                    [("class_name","DataGridCell"),("name",f".*0")],
                    [("name",f".*{row_label}.*")]
                    # [("class_name","ComboBox")],
                    # [("name","EmbeddedTextbox")]
                ]
                el = actions.user.find_el_by_prop_seq(prop_seq,row,verbose = True)
                if el:
                    output_row = row
                    break
            print(f'output_row: {output_row}')
            if output_row:
                actions.user.act_on_element(output_row,"invoke")
                    
    def arc_tool_properties_select_column(col: int):
        """selects the sell in the current row given column"""
       # obtain grid
        grid = None
        root = winui.active_window().element
        if root:
            prop_seq = [
                [("class_name","ListPropertySheet")],
                [("class_name","PageHost")],
                [("class_name","ToolParametersView")],
                [("class_name","EditSafeDataGrid")]
            ]
            grid = actions.user.find_el_by_prop_seq(prop_seq,root)
            if grid:
                # obtain current data grid row
                row = None
                prop_list = [("class_name","DataGridRow")]
                el = winui.focused_element()
                if el:
                    row = actions.user.matching_ancestor(el,prop_list)
                if not row:
                    prop_list = [("class_name","DataGridRow")]
                    row = actions.user.matching_child(grid,prop_list)
                if row:
                    prop_list = [("class_name","DataGridCell"),("name",f".*Column Display Index: {col}")]
                    el = actions.user.matching_child(row,prop_list)
                    if el:
                        # This causes errors for Data Type (column #2)
                        if col == "2":
                            # Need to handle DATA TYPE column differently
                            # as it opens up a dialog which seems to cause UIAutomation 
                            # to stall if it gets any other requests (e.g. from auto highlight)
                            # According to Google AI:
                            # When using UI Automation (UIA) to interact with a Windows application, particularly when invoking actions on UI elements (like buttons, menu items, etc.), it's often recommended to do so from a separate "helper thread" instead of your application's main UI thread.
                            # Also see:
                            # https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-threading
                            # C:\Users\barry\CaGIS Board Dropbox\cantaloupe bob\Barry\Technology\Invoking UI Automation with a helper thread.docx
                            actions.user.act_on_element(el,"click")
                        else:
                            actions.user.act_on_element(el,"invoke")
                        
ctx = Context()
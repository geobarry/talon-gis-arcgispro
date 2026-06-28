from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax, ui as winui

mod = Module()

@mod.action_class
class Actions:
    def arc_get_python_window():
        """returns python window element"""
        root = winui.active_window().element
        prop_seq = [
            [("class_name","FrameworkDockSite")],
            [("class_name","DockHost")],
            [("class_name","SplitContainer")],
            [("class_name","ToolWindowContainer")],
            [("class_name","ToolWindow")],
            [("class_name","PythonWindowView")],
            [("class_name","RichTextBox")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        print("FUNCTION: arc_get_python_window")
        print(f'el: {el}')
        if actions.user.element_match(el,prop_seq[-1]):
            actions.user.act_on_element(el,"select")
            return el
        else:
            return None
    def arc_python_text(t: str = ""):
        """writes code into the python window"""
        w = actions.user.arc_get_python_window()
        if w:
            actions.insert(t)
        
        
            
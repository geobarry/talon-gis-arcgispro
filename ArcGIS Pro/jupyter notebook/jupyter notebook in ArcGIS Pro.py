from talon import Context,Module,actions,clip,ui,ctrl,settings
from talon.windows import ax as ax, ui as winui

mod = Module()

mod.list("jupyter_toolbar_command","property sequence string to get from toolbar to command")

def arc_jupyter_toolbar():
    root = winui.active_window().element
    prop_seq = [
        [("class_name","FrameworkDockSite")],
        [("class_name","DockHost")],
        [("class_name","SplitContainer")],
        [("class_name","Workspace")],
        [("class_name","TabbedMdiContainer")],
        [("class_name","DockingWindowContainerTabItem")],
        [("class_name","DocumentWindow")],
        [("class_name","ProNotebookPaneView")],
        [("class_name","HwndHost")],
        [("class_name","Static")],
        [("class_name","Chrome_WidgetWin_0")],
        [("class_name","Chrome_WidgetWin_1")],
        [("class_name","BrowserRootView")],
        [("class_name","NonClientView")],
        [("class_name","EmbeddedBrowserFrameView")],
        [("class_name","BrowserView")],
        [("class_name","SidebarContentsSplitView")],
        [("class_name","SidebarContentsSplitView")],
        [("class_name","View")],
        [("automation_id","RootWebArea")],
        [],
        [("class_name","lm-Widget lm-Panel")],
        [("class_name","lm-Widget jp-MainAreaWidget jp-NotebookPanel jp-Document jp-mod-searchable")],
        [("class_name","lm-Widget jp-Toolbar jp-NotebookPanel-toolbar")],
    ]
    el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
    return el

@mod.action_class
class Actions:
    def arc_invoke_jupyter_command(prop_seq_str: str):
        """invokes button within a jupyter notebook"""
        el = arc_jupyter_toolbar()
        prop_str_list = prop_seq_str.split(";")
        prop_seq = [actions.user.get_property_list(x) for x in prop_str_list]
        el = actions.user.find_el_by_prop_seq(prop_seq,el)
        if "Invoke" in el.patterns:
            actions.user.act_on_element(el,"invoke")
        else:
            actions.user.act_on_element(el,"expand")

    def arc_go_to_jupyter_content():
        """navigates to jupyter notebook content cells"""
        root = winui.active_window().element
        prop_seq = [
                    [("name",""),("class_name","FrameworkDockSite")],
                    [("name",""),("class_name","DockHost")],
                    [("name",""),("class_name","SplitContainer")],
                    [("name",""),("class_name","Workspace")],
                    [("name",""),("class_name","TabbedMdiContainer")],
                    [("name","New Notebook"),("class_name","DockingWindowContainerTabItem")],
                    [("name","New Notebook"),("class_name","DocumentWindow")],
                    [("name",""),("class_name","ProNotebookPaneView")],
                    [("name",""),("class_name","HwndHost")],
                    [("name",""),("class_name","Static")],
                    [("name",""),("class_name","Chrome_WidgetWin_0")],
                    [("name","New Notebook"),("class_name","Chrome_WidgetWin_1")],
                    [("name","New Notebook - Web content"),("class_name","BrowserRootView")],
                    [("name",""),("class_name","NonClientView")],
                    [("name",""),("class_name","EmbeddedBrowserFrameView")],
                    [("name",""),("class_name","BrowserView")],
                    [("name",""),("class_name","SidebarContentsSplitView")],
                    [("name",""),("class_name","SidebarContentsSplitView")],
                    [("name",""),("class_name","View")],
                    [("name","New Notebook"),("class_name","")],
                    [("name",""),("class_name","")],
                    [("name",""),("class_name","lm-Widget lm-Panel")],
                    [("name",""),("class_name","lm-Widget jp-MainAreaWidget jp-NotebookPanel jp-Document jp-mod-searchable")],
                    [("name","notebook content"),("class_name","jp-WindowedPanel lm-Widget jp-Notebook jp-mod-scrollPastEnd jp-mod-showHiddenCellsButton jp-NotebookPanel-notebook jp-mod-commandMode")],
            ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        actions.user.act_on_element(el,"click")

    def arc_go_to_jupyter_cell(cell_num: int = 1):
        """navigate to the designated cell. Virtual scrollbar must be visible."""
        root = winui.active_window().element
        prop_seq = [
                [("class_name","FrameworkDockSite")],
                [("class_name","DockHost")],
                [("class_name","SplitContainer")],
                [("class_name","Workspace")],
                [("class_name","TabbedMdiContainer")],
                [("name","Scale Specific Sinuosity"),("class_name","DockingWindowContainerTabItem")],
                [("name","Scale Specific Sinuosity"),("class_name","DocumentWindow")],
                [("class_name","ProNotebookPaneView")],
                [("class_name","HwndHost")],
                [("class_name","Static")],
                [("class_name","Chrome_WidgetWin_0")],
                [("name","Scale Specific Sinuosity"),("class_name","Chrome_WidgetWin_1")],
                [("name","Scale Specific Sinuosity - Web content"),("class_name","BrowserRootView")],
                [("class_name","NonClientView")],
                [("class_name","EmbeddedBrowserFrameView")],
                [("class_name","BrowserView")],
                [("class_name","SidebarContentsSplitView")],
                [("class_name","SidebarContentsSplitView")],
                [("class_name","View")],
                [("name","Scale Specific Sinuosity"),("class_name","")],
                [("class_name","")],
                [("class_name","lm-Widget lm-Panel")],
                [("class_name","lm-Widget jp-MainAreaWidget jp-NotebookPanel jp-Document jp-mod-searchable")],
                [("name","notebook content")],
                [("class_name","jp-WindowedPanel-scrollbar-content")],
                [("name",str(cell_num))]
            ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
        print(f'JUPYTER NOTEBOOK el: {el.name}')
        for child in el.children:
            print(f'child: name {child.name} | class {child.class_name}')
        actions.sleep(0.5)
        actions.user.act_on_element(el,"click")



from talon import Module, Context, actions, ctrl

compass_diffs = {
    0.0: (0,-1),
    180.0: (0,1),
    90.0: (1,0),
    270.0: (-1,0)
}

mod=Module()

arcgis_pro_ctx=Context()
arcgis_pro_ctx.matches = r"""
app.exe: arcgispro.exe
"""

@mod.capture(rule="north|east|south|west")
def four_directions(m) -> float:
    """north southeast or west converted to a number"""
    match str(m):
        case 'north':
            return 0.0
        case 'east':
            return 90.0
        case 'south':
            return 180.0
        case 'west':
            return 270.0

@arcgis_pro_ctx.action_class('self')
class Actions:
    def drag_window_center(bearing: float, d: float):
        """Pans the map by the given percent"""
        # start in the center of the map or layout
        root = actions.user.earthbound_root()
        prop_seq = [
        	[("control_type","Group"),("automation_id","dockSite")],
        	[("control_type","Group"),("automation_id","dockSite.PART_DockHost")],
        	[("control_type","Group")],
        	[("control_type","Group")],
        	[("control_type","Group")],
        	[("control_type","Pane")],
        	[("control_type","Tab"),("automation_id",".*Workspace__TabbedMdiContainer")],
        	[("control_type","TabItem"),("automation_id","esri_mapping_mapPane_275Tab")],
        	[("control_type","Pane"),("automation_id","esri_mapping_mapPane_275")],
        	[("control_type","Custom")],
        	[("control_type","Custom"),("automation_id","MapControl")],
        	[("control_type","Pane")]
        ]
        el = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = False)
        if el:
            # Max shift in one go is 49%
            print(f'map pan d: {d}')
            if d > 49:
                d=49
            print(f'map pan d: {d}')
            # Calculate position for mouse
            rect=actions.user.el_prop_val(el,'rect')
            wd=rect.width
            ht=rect.height
            dx,dy=compass_diffs[bearing]
            dx *= d
            dy *= d
            print(f'dx: {dx}')
            print(f'dy: {dy}')
            x = el.rect.x + wd * (50 + dx) / 100
            y = el.rect.y + ht * (50 + dy) / 100
            # click to recenter
            ctrl.mouse_move(x,y)
            actions.key("ctrl:down")
            ctrl.mouse_click(0)
            actions.key("ctrl:up")

                

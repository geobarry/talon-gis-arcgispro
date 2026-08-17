from talon import Module, actions

mod=Module()

@mod.action_class
class colordialogActions:
    def arc_color_dialog_property(prop_name: str, prop_val: str = ""):
        """navigates to the given property in the color dialog"""
        with actions.user.tracking_paused():
            # obtain editor control container
            root = actions.user.window_root()
            prop_seq = [
                [("automation_id","ColorEditorControl")],
            ]
            container = actions.user.find_el_by_prop_seq(prop_seq,root,verbose = True)
            if container:
                # controls that we need are not labeled so need to look for TextBlock label which precedes it
                prop_list=[("name",prop_name), ("class_name","TextBlock")]
                children=actions.user.el_prop_val(container,'children')
                if children:
                    lbl_el=actions.user.matching_child(container,prop_list)
                    if lbl_el:
                        lbl_el_idx=children.index(lbl_el)
                        # control that we need is the next element in sequence or else a descendant of the next element
                        child_el=children[lbl_el_idx + 1]
                        if child_el:
                            # ultimately we are looking for a textbox element
                            txt_el=None
                            if actions.user.element_match(child_el,[("class_name","TextBox")]):
                                txt_el=child_el
                            # if we have got a spinner we need to dig down one more level
                            elif actions.user.element_match(child_el,[("control_type","spinner")]):
                                prop_list=[("class_name","TextBox")]
                                txt_el=actions.user.matching_child(child_el,prop_list)
                            # once we have textbox element, select the text inside and return the element
                            if txt_el:
                                actions.user.act_on_element(txt_el,'select')
                                actions.key("ctrl-a")
                                if prop_val != "":
                                    actions.insert(prop_val)
                                return txt_el                                
        
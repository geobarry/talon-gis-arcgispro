from talon import Module, actions

mod=Module()

@mod.action_class
class Actions:
    def arc_label_class_fields():
        """Places focus on the fields list box in the label class panel"""
        # unable to get to it via automation alone so start with Label Expression sub tab
        actions.user.arc_label_group('.*LabelClass.*','Label Expression')
        # then use tab key
        actions.user.key_to_matching_element("tab",[("name","Field List")])
from enthought.traits.ui.api import Group, Item

error_string_group = Group(
    Item('error_string',
        show_label=False,
        style='readonly',
        emphasized=True,
    ),
#    visible_when='len(object.error_string) > 0',
    enabled_when='len(object.error_string) > 0',
    label='Error(s)',
)
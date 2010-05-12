from infobiotics.shared.traits_imports import *


plot_action = Action(
    name='Plot',
    action='plot',
    tooltip='Plot results with current options',
#    enabled_when='object.has_valid_parameters()',
)


save_data_action = Action(
    name='Save data',
    action='save_data',
    tooltip='Save results with current options',
    enabled_when='False',
)


show_script_action = Action(
    name='Show script',
    action='show_script',
    tooltip='Display the script equivalent to current options',
)

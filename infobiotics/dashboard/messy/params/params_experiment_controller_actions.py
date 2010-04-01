from enthought.traits.ui.api import Action
from infobiotics.dashboard.params.api import load_action, save_action

perform_action = Action(name='Perform', action='perform', 
    tooltip='Perform the experiment with the current parameters',
    enabled_when='object.has_valid_parameters()', #XXX calls has_valid_parameters which each UI change
)

load_save_perform_actions = [load_action, save_action, perform_action] 
from enthought.traits.ui.api import Action

load_action = Action(name='Load', action='load', 
    tooltip='Load parameters from a file'
) 

save_action = Action(name='Save', action='save', 
    tooltip='Save the current parameters to a file'
)

load_save_actions = [load_action, save_action]
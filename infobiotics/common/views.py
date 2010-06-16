'''
Views, Groups, Items, Actions and KeyBindings that are common to ParamsHandler
subclasses.
'''

from enthought.traits.ui.menu import Action
from enthought.traits.ui.api import View, HGroup, VGroup, Item, StatusItem

load_action = Action(
    name='&Load', 
    action='load', 
    tooltip='Load parameters from a file'
) 

save_action = Action(
    name='&Save', 
    action='save', 
    tooltip='Save the current parameters to a file'
)

perform_action = Action(
    name='&Perform', 
    action='perform', 
    tooltip='Perform the experiment with the current parameters',
#    enabled_when='controller.has_valid_parameters',
    enabled_when='handler.has_valid_parameters',
)

shared_actions = [ # ParamsView and ExperimentView
    'Undo',
] 

#from infobiotics.commons.traits.ui.api import help_action

#shared_actions = shared_actions + ['Help'] # TraitsUI help which doesn't work in TraitsBackendQt
#shared_actions = shared_actions + [help_action]

params_actions = [ # ParamsView only
#    load_action, 
#    save_action, 
    'OK',
]

experiment_actions = [ # ExperimentView only
#    load_action, 
#    save_action, 
    perform_action, 
    'Cancel',
]

from enthought.traits.ui.menu import Menu, MenuBar, ToolBar

file_menu = Menu(
    load_action, save_action,
    name = '&File'
)

#TODO about_action

toolbar = ToolBar(load_action, save_action)

executable_group = HGroup(
    Item('executable', 
        label='Program',
        visible_when='"Dashboard" not in handler.__class__.__name__', 
    ),
    visible_when='object.__class__.__name__ not in ("McssParams", "POptimizerParams")', # only needed for PRISMParams (and MC2Params? TODO)
) 

directory_group = HGroup(
    Item('directory', 
        label='Current working directory', 
        tooltip='Relative paths will be resolved to this directory.',
    ),
)

class ParamsView(View): # can be used to edit parameters without performing the experiment (why would you want to do that?)
    
    buttons = shared_actions + params_actions
    
    resizable = True

    toolbar = toolbar

    statusbar = [ 
        StatusItem(
            name='handler.status',
            width=1.0
        ),
    ]

    def set_content(self, *values):
        values = [
            VGroup(
                executable_group, #TODO could move executable_group to ExperimentView but for PModelChecker running itself to create modelParameters.xml and PRISM_model
                directory_group,
#                '_',
                values,
                show_border=True,
            ),
        ]
        super(ParamsView, self).set_content(*values)
        
    
class ExperimentView(ParamsView):
    
    buttons = shared_actions + experiment_actions
        
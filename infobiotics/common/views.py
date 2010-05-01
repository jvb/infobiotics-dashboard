'''
Views, Groups, Items, Actions and KeyBindings that are common to ParamsHandler
subclasses.
'''

from enthought.traits.ui.api import Action, View, HGroup, VGroup, Item, StatusItem

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

help_action = Action(
    name='&Help', 
    action='help',
    visible_when='handler.has_help', # see ParamsHandler  
)

#shared_actions = shared_actions + ['Help'] # TraitsUI help which doesn't work in TraitsBackendQt
shared_actions = shared_actions + [help_action]

params_actions = [ # ParamsView only
    load_action, 
    save_action, 
    'OK',
]

experiment_actions = [ # ExperimentView only
    load_action, 
    save_action, 
    perform_action, 
    'Cancel',
]

_params_program_group = HGroup(
    Item('_params_program', 
        label='Program',
        visible_when='"Dashboard" not in handler.__class__.__name__', 
    ),
) 

_cwd_group = HGroup(
    Item('_cwd', 
        label='Current working directory', 
        tooltip='Relative paths will be resolved to this directory.',
    ),
)

class ParamsView(View): # can be used to edit parameters without performing the experiment (why would you want to do that?)
    buttons = shared_actions + params_actions
    resizable = True

#    id = 'ParamsView' # instances should define their own id 

#    statusbar = [
##        StatusItem(
##            name='_cwd', # better to be editable: use '_cwd_group' above
##            width=1.0
##        ),
#    ]

#    # better to allow instances to choose where to put '_cwd_group'
#    # can't add top-level group with show_border=True to values either (really?)
##    def set_content(self, *values): #TODO check this
##        values = [_cwd_group] + list(values)
##        super(ParamsView, self).set_content(*values) 
    def set_content(self, *values):
        values = [
            VGroup(
                _cwd_group,
#                '_',
                values,
                _params_program_group,
                show_border=True,
            ),
        ]
        super(ParamsView, self).set_content(*values)
        
    
class ExperimentView(ParamsView):
    buttons = shared_actions + experiment_actions

#def test_ParamsView_set_content():
#    from enthought.traits.api import HasTraits, Int
#    class Test(HasTraits):
#        _cwd = Int
#        i = Int
#        view = ParamsView(
#            'i',
#        )
#    test = Test()
#    test.configure_traits()
#    
#if __name__ == '__main__':
#    test_ParamsView_set_content()
#        
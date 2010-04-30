'''
Views, Groups, Items, Actions and KeyBindings that are common to ParamsHandler
subclasses.
'''

from enthought.traits.ui.api import Action, View, HGroup, VGroup, StatusItem
from enthought.traits.ui.key_bindings import *

params_key_bindings = KeyBindings(
    KeyBinding(
        binding1    = 'Ctrl-L',
        description = 'Load',
        method_name = 'load',
    ),
    KeyBinding(
        binding1    = 'Ctrl-S',
        description = 'Save',
        method_name = 'save',
    ),
    KeyBinding(
        binding1    = 'Ctrl-P',
        description = 'Perform',
        method_name = 'perform',
    ),
    KeyBinding(
        binding1    = 'Ctrl-K',
        description = 'Edit key bindings',
        method_name = 'edit_key_bindings',
    ),
)

def edit_key_bindings(self):
    params_key_bindings.edit_traits(kind='modal') #TODO check this

load_action = Action(name='&Load', action='load', 
    tooltip='Load parameters from a file'
) 

save_action = Action(name='&Save', action='save', 
    tooltip='Save the current parameters to a file'
)

perform_action = Action(name='&Perform', action='perform', 
    tooltip='Perform the experiment with the current parameters',
#    enabled_when='controller.has_valid_parameters',
    enabled_when='handler.has_valid_parameters',
)

shared_actions = [ # ParamsView and ExperimentView
    'Undo',
] 

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

_cwd_group = HGroup(
    Item('_cwd', 
        label='Current working directory', 
        tooltip='Relative paths will be resolved to this directory.',
    ),
)

class ParamsView(View): # can be used to edit parameters without performing the experiment (why would you want to do that?)
    buttons = params_actions + shared_actions
    resizable = True
    key_bindings = params_key_bindings

#    id = 'ParamsView' # instances should define their own id 

#    statusbar = [
##        StatusItem(
##            name='_cwd', # better to be editable: use '_cwd_group' above
##            width=1.0
##        ),
#    ]

    # better to allow instances to choose where to put '_cwd_group'
    # can't add top-level group with show_border=True to values either (really?)
#    def set_content(self, *values): #TODO check this
#        values = [_cwd_group] + list(values)
#        super(ParamsView, self).set_content(*values) 
    
class ExperimentView(ParamsView):
    buttons = experiment_actions + shared_actions

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
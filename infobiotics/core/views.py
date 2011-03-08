'''
Views, Groups, Items, Actions and KeyBindings that are shared by ParamsHandler
subclasses.
'''

from enthought.traits.ui.menu import Action
from enthought.traits.ui.api import View, HGroup, VGroup, Item, StatusItem

close_action = Action(
    name='&Close',
#    action='_on_close', # doesn't terminate event loop if last window closed 
    action='close_window', # in ParamsHandler; calls info.ui.control.close() 
) 

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
    load_action, save_action, close_action,
    name='&File'
)

#TODO about_action

toolbar = ToolBar(load_action, save_action)

#from enthought.traits.ui.api import TextEditor
#status_group = HGroup( # better than status bar because long texts can be shown
#    Item('handler.status',
#        show_label=False,
#        editor=TextEditor(),
#        style='readonly',
#    ),
#    visible_when='len(handler.status) > 0'
#)

directory_group = HGroup(
    Item('directory',
#        tooltip='Relative file paths will be resolved to this directory.',
    ),
)

class ParamsView(View): # can be used to edit parameters without performing the experiment (why would you want to do that?)
    
    buttons = shared_actions + params_actions
    
    resizable = True
    width = 560
    height = 560
    scrollable = True

    toolbar = toolbar
    
    statusbar = [ 
        StatusItem(
            name='handler.status',
            width=1.0,
        ),
    ]

    def set_content(self, *values):
        values = [
            VGroup(
#                status_group,
                directory_group,
#                '_',
                values,
                show_border=True,
            ),
        ]
        super(ParamsView, self).set_content(*values)
        
    
class ExperimentView(ParamsView):
    
    buttons = shared_actions + experiment_actions
        

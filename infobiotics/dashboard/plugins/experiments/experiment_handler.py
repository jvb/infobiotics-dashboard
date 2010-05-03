from enthought.traits.ui.api import Handler
from enthought.traits.api import implements, Bool
from i_experiment_handler import IExperimentHandler
#from enthought.traits.ui.ui_info import UIInfo

class ExperimentHandler(Handler):
    ''' Standard handler for Experiment actions.
    
    Required for TraitsUI action buttons, it simply calls the synonymous 
    functions on the experiment pointed to by 'info.object', i.e. it wraps the 
    scripting interface.
    
    Also used to decide whether the experiment is interactive or not.
    
    '''
    implements(IExperimentHandler)   

    def perform(self, info):
        ''' Perform the experiment.
        
        '''
        info.object.perform()

    interactive = Bool(False)
    
    def is_interactive(self):
        ''' Returns whether the experiment is being manipulated with through a
        TraitsUI window (interactive) or as part of a script (non-interactive).
        
        '''
        return self.interactive
    
    def init(self, info):
        ''' Sets 'interactive' to True when Handler is initialised.
        
        Subclasses that override 'init()' *should* call it using super():
            "super(self, SubclassOfExperimentHandler).init(info)"
        
        'info' is not an attribute of Handler so we could save it here. 
        
        '''
        self.interactive = True

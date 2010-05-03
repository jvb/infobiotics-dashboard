from enthought.traits.api import Interface, Instance
from experiment_handler import ExperimentHandler

class IExperiment(Interface):
    ''' Defines the interface for an experiment can be performed.
    
    '''
        
    def perform(self):
        ''' Performs the experiment.
        
        '''
    
    handler = Instance(ExperimentHandler)
    
    def is_part_of_application(self):
        ''' Returns whether the experiment is part of an Envisage application 
        (created by an Action).
        
        '''
    
    def is_interactive(self):
        ''' Returns whether the experiment is being manipulated with through a
        TraitsUI window (interactive) or as part of a script (non-interactive).
        
        '''

    def create_progress_meter(self, **traits):
        ''' Returns an appropriate progress meter for the current mode of 
        operation.
        
        '''
            
from enthought.traits.api import HasTraits, implements, Instance
from i_experiment import IExperiment
from experiment_handler import ExperimentHandler

class Experiment(HasTraits):
    ''' Abstract base class of all Infobiotics Dashboard experiments.
    
    '''
    implements(IExperiment)

    def perform(self):
        ''' Performs the experiment.
        
        '''
        raise NotImplementedError(
            'Subclasses of Experiment must reimplement perform()'
        )


    handler = Instance(ExperimentHandler)

    def has_application(self):
        ''' Returns whether the experiment is part of an Envisage application 
        (created by an Action).
        
        '''
        if hasattr(self, 'application'):
            if self.application is not None:
                return True
        return False

    def is_part_of_application(self):
        ''' Returns whether the experiment is part of an Envisage application 
        (created by an Action).
        
        '''
        return self.has_application()

    def is_interactive(self):
        ''' Returns whether the experiment is being manipulated with through a
        TraitsUI window (interactive) or as part of a script (non-interactive).
        
        '''
        if self.is_part_of_application():
            return True
        else:
            return self.handler.is_interactive()

    def create_progress_meter(self, **traits): #TEST
        ''' Returns an appropriate progress meter for the current mode of 
        operation.
        
        '''
        if self.is_interactive():
            if self.is_part_of_application():
#                from progress_item import ProgressItem as ProgressMeter
                from experiment_progress_item import ExperimentProgressItem as ProgressMeter
            else:
                from progress_dialog import ProgressDialog
                return ProgressDialog( 
                    title=self.name, 
                    message=traits['text'] if 'text' in traits else '', 
                    max=traits['max'] if 'max' in traits else 0,
                    min=traits['min'] if 'min' in traits else 0,
                    show_percent=True,                     
#                    show_time=True,
                    can_cancel=True,
#                    cancel_button_label='Cancel',
#                    can_ok=False,
#                    margin=5,
                )
        else:
            from noninteractive_progress_meter import NoninteractiveProgressMeter as ProgressMeter
        return ProgressMeter(**traits)

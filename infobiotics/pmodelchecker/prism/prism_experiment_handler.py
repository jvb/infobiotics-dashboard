from infobiotics.pmodelchecker.prism.api import PRISMParamsHandler, PRISMExperimentProgressHandler 
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class PRISMExperimentHandler(PRISMParamsHandler, PModelCheckerExperimentHandler):
    
    def __progress_handler_default(self):
        return PRISMExperimentProgressHandler(model=self.model)

#    def object_finished_changed(self, info):
#        ''' Triggered when experiment's expect loop finishes. '''
#        self._progress_handler.message = 'Loading results...' # doesn't change the message!
#        self.show_results() # PModelCheckerExperimentHandler.show_results() #TODO


if __name__ == '__main__':
    execfile('prism_experiment.py')
    
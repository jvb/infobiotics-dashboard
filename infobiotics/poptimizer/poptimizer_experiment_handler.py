from poptimizer_params_handler import POptimizerParamsHandler
from infobiotics.core.experiment_handler import ExperimentHandler
from poptimizer_experiment_progress_handler import POptimizerExperimentProgressHandler
from poptimizer_results import POptimizerResults

class POptimizerExperimentHandler(POptimizerParamsHandler, ExperimentHandler):
    
    def __progress_handler_default(self):
        return POptimizerExperimentProgressHandler(model=self.model)

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
#        self._progress_handler.message = 'Loading results...' # doesn't change the message!
        self.show_results()
        
    def show_results(self):
        POptimizerResults(experiment=self.model).edit_traits()


if __name__ == '__main__':
    execfile('poptimizer_experiment.py')
    
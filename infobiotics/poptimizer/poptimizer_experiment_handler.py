from poptimizer_params_handler import POptimizerParamsHandler
from infobiotics.core.experiment_handler import ExperimentHandler
from poptimizer_results import POptimizerResults

class POptimizerExperimentHandler(POptimizerParamsHandler, ExperimentHandler):
    
    def show_results(self):
        POptimizerResults(experiment=self.model).edit_traits()


if __name__ == '__main__':
    execfile('poptimizer_experiment.py')

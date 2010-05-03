from poptimizer_params_handler import POptimizerParamsHandler
from infobiotics.common.api import ExperimentHandler
from poptimizer_experiment_progress_handler import POptimizerExperimentProgressHandler

class POptimizerExperimentHandler(POptimizerParamsHandler, ExperimentHandler):
    
    _progress_handler = POptimizerExperimentProgressHandler


if __name__ == '__main__':
    execfile('poptimizer_experiment.py')
    
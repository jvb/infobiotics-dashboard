from infobiotics.common.api import ExperimentHandler
from poptimizer_experiment_progress_handler import POptimizerExperimentProgressHandler

class POptimizerExperimentHandler(ExperimentHandler):
    
    _progress_handler = POptimizerExperimentProgressHandler
        
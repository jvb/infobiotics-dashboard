from infobiotics.core.experiment import Experiment

class PModelCheckerExperiment(Experiment): #TODO remove if this is useless 

    _parameters_name = 'pmodelchecker'

    _stderr_pattern_list = [
        'Exception in thread "main" java',
    ] 

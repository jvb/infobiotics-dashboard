from infobiotics.pmodelchecker.prism.api import PRISMParamsHandler, PRISMExperimentProgressHandler 
from infobiotics.common.api import ExperimentHandler

class PRISMExperimentHandler(PRISMParamsHandler, ExperimentHandler):
    
    _progress_handler = PRISMExperimentProgressHandler


if __name__ == '__main__':
    execfile('prism_experiment.py')
    
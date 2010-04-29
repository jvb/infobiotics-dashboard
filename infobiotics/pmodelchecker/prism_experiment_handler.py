from infobiotics.shared.api import ExperimentView
from infobiotics.pmodelchecker.api import prism_params_group, PModelCheckerExperimentHandler, PRISMParamsHandler, PRISMExperimentProgressHandler

prism_experiment_view = ExperimentView(
    prism_params_group,
    id = 'prism_experiment_view',
) 

class PRISMExperimentHandler(PModelCheckerExperimentHandler, PRISMParamsHandler):
    
    traits_view = prism_experiment_view 
    
    _progress_handler = PRISMExperimentProgressHandler


if __name__ == '__main__':
    execfile('prism_experiment.py')
    
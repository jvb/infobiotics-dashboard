from infobiotics.common.api import ExperimentView
from infobiotics.pmodelchecker.api import PModelCheckerExperimentHandler
from prism_params_group import prism_params_group
from prism_params_handler import PRISMParamsHandler
from prism_experiment_progress_handler import PRISMExperimentProgressHandler 

prism_experiment_view = ExperimentView(
    prism_params_group,
    id = 'prism_experiment_view',
) 

class PRISMExperimentHandler(PModelCheckerExperimentHandler, PRISMParamsHandler):
    
    traits_view = prism_experiment_view 
    
    _progress_handler = PRISMExperimentProgressHandler


if __name__ == '__main__':
    execfile('prism_experiment.py')
    
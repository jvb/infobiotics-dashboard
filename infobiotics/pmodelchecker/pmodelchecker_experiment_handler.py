from infobiotics.shared.api import (
    ExperimentView, ExperimentHandler, 
)
from infobiotics.pmodelchecker.api import prism_params_group

prism_experiment_view = ExperimentView(
    prism_params_group,
)

class PModelCheckerExperimentHandler(ExperimentHandler):
    
    traits_view = prism_experiment_view
    id = 'PModelCheckerExperimentHandler'
    
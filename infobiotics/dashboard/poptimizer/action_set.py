from envisage.ui.workbench.api import WorkbenchActionSet
from envisage.ui.action.api import Action
            
class POptimizerActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.poptimizer.action_set:POptimizerActionSet'

    actions = [
        Action(path='MenuBar/Experiments', class_name='infobiotics.dashboard.poptimizer.actions:POptimizerExperimentAction'),
        Action(path='ToolBar/Experiments', class_name='infobiotics.dashboard.poptimizer.actions:POptimizerExperimentAction'),
    ]

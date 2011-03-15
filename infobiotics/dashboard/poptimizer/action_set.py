from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action
            
class POptimizerActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.plugins.poptimizer.action_set:POptimizerActionSet'

    actions = [
        Action(path='MenuBar/Experiments', class_name='infobiotics.dashboard.plugins.poptimizer.actions:POptimizerExperimentAction'),
        Action(path='ToolBar/Experiments', class_name='infobiotics.dashboard.plugins.poptimizer.actions:POptimizerExperimentAction'),
    ]

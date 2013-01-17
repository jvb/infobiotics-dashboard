from envisage.ui.workbench.api import WorkbenchActionSet
from envisage.ui.action.api import Group, Action
            
class PModelCheckerActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.pmodelchecker.action_set'

    actions = [
        Action(
#            name='Open &PModelChecker results...', 
            class_name='infobiotics.dashboard.pmodelchecker.actions:PModelCheckerResultsAction',
            group='ResultsGroup',
            path='MenuBar/File', 
        ),

        Action(path='MenuBar/Experiments', class_name='infobiotics.dashboard.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='ToolBar/Experiments', class_name='infobiotics.dashboard.pmodelchecker.actions:PRISMExperimentAction'),

        Action(path='MenuBar/Experiments', class_name='infobiotics.dashboard.pmodelchecker.actions:MC2ExperimentAction'),
        Action(path='ToolBar/Experiments', class_name='infobiotics.dashboard.pmodelchecker.actions:MC2ExperimentAction'),
    ]

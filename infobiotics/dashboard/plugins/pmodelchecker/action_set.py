from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import ToolBar, Action
            
class PModelCheckerActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.plugins.pmodelchecker.action_set'

    tool_bars = [
        ToolBar(
            id='Results', 
        ),
    ]
        
    actions = [
        Action(
            path='MenuBar/Results', 
            name='PModelChecker',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PModelCheckerResultsAction',
        ),
        Action(
            path='ToolBar/Results', 
            name='PModelChecker',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PModelCheckerResultsAction',
        ),
        Action(path='MenuBar/Experiment', name='Model checking (PRISM)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='MenuBar/Experiment', name='Model checking (MC2)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
        Action(path='ToolBar/Experiment', name='Model checking (PRISM)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='ToolBar/Experiment', name='Model checking (MC2)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
    ]

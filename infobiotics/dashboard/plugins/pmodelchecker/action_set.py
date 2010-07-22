from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action
            
class PModelCheckerActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.plugins.pmodelchecker.action_set'

    actions = [
        
        # Experiment menu
        Action(path='MenuBar/Experiment', name='Model checking (PRISM)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='MenuBar/Experiment', name='Model checking (MC2)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
        
        # Experiment toolbar
        Action(path='ToolBar/Experiment', name='Model checking (PRISM)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='ToolBar/Experiment', name='Model checking (MC2)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
    ]

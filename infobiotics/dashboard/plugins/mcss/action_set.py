from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action
            
class McssActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.plugins.mcss.action_set.McssActionSet'

    actions = [
        Action(path='MenuBar/Experiments', class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
        Action(path='ToolBar/Experiments',  class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
    ]

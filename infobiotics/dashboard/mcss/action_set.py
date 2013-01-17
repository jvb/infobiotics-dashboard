from envisage.ui.workbench.api import WorkbenchActionSet
from envisage.ui.action.api import Group, Action
            
class McssActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.mcss.action_set.McssActionSet'

    actions = [
        Action(path='MenuBar/Experiments', class_name='infobiotics.dashboard.mcss.actions:McssExperimentAction'),
        Action(path='ToolBar/Experiments', class_name='infobiotics.dashboard.mcss.actions:McssExperimentAction'),
    ]

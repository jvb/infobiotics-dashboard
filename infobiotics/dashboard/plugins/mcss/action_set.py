from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from actions import McssExperimentAction
            
class McssActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.plugins.mcss.action_set.McssActionSet'

    groups = [
#        Group(id='McssGroup', path='MenuBar/Experiment'),
    ]
        
    menus = [
             
        # Experiment menu
        Menu(
            name='Experiment', path='MenuBar', before='View',
            groups=['McssGroup']
        ),
    ]

    tool_bars = [
        ToolBar(id='Experiment', groups=['McssGroup']),
    ]
        
    actions = [
        
        # Experiment menu
        Action(path='MenuBar/Experiment', name='Simulation (mcss)',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
        
        # Experiment toolbar
        Action(path='ToolBar/Experiment', name='Simulation (mcss)',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
    ]

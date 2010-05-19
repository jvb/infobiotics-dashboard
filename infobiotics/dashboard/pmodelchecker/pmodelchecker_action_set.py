#from actions import *
from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet
            
            
class PModelCheckerActionSet(WorkbenchActionSet):
    
    # 'WorkbenchActionSet' interface
#    enabled_for_perspectives = ['Experiments'] # The Ids of the perspectives that the action set is enabled in
#    visible_for_perspectives = ['BNF','Foo'] # The Ids of the perspectives that the action set is visible in
#    enabled_for_views = ['Red'] # The Ids of the views that the action set is enabled for
#    visible_for_views = ['Red'] # The Ids of the views that the action set is visible for

    # 'ActionSet' interface
    id = 'infobiotics.dashboard.plugins.pmodelchecker.pmodelchecker_action_set' # The action set's globally unique identifier

    groups = [
    ]
        
    menus = [
    ]

    tool_bars = [
        ToolBar(name='PModelChecker', id='PModelChecker toolbar', path='ToolBar/Experiment'),
    ]
        
    actions = [
        
        # Experiment menu
#        Action(path='MenuBar/Experiment', name='PModelChecker',
#            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:NewPModelCheckerAction'),
        Action(path='MenuBar/Experiment', name='PRISM',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='MenuBar/Experiment', name='MC2',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
#        Action(path='MenuBar/Experiment', name='PModelChecker',
#            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:'),
        
        # Experiment toolbar
#        Action(path='ToolBar/Experiment', name='PModelChecker',
#            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:NewPModelCheckerAction'),
        Action(path='ToolBar/Experiment', name='PRISM',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='ToolBar/Experiment', name='MC2',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
#        Action(path='ToolBar/Experiment', name='PModelChecker',
#            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:'),
    ]

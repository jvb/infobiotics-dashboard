from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action#, Group, Menu, ToolBar
from actions import POptimizerExperimentAction
            
class POptimizerActionSet(WorkbenchActionSet):
    
    # 'WorkbenchActionSet' interface
#    enabled_for_perspectives = ['Experiments'] # The Ids of the perspectives that the action set is enabled in
#    visible_for_perspectives = ['BNF','Foo'] # The Ids of the perspectives that the action set is visible in
#    enabled_for_views = ['Red'] # The Ids of the views that the action set is enabled for
#    visible_for_views = ['Red'] # The Ids of the views that the action set is visible for

    # 'ActionSet' interface
    id = 'infobiotics.dashboard.plugins.poptimizer.poptimizer_action_set' # The action set's globally unique identifier

    groups = [
    ]
        
    menus = [
    ]

    tool_bars = [
    ]
        
    actions = [
        
        # Experiment menu
        Action(path='MenuBar/Experiment', name='Optimisation (POptimizer)',
            class_name='infobiotics.dashboard.plugins.poptimizer.actions:POptimizerExperimentAction'),
        
        # Experiment toolbar
        Action(path='ToolBar/Experiment', name='Optimisation (POptimizer)',
            class_name='infobiotics.dashboard.plugins.poptimizer.actions:POptimizerExperimentAction'),
    ]

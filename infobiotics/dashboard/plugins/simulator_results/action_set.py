from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from actions import SimulatorResultsAction
            
class  SimulatorResultsActionSet(WorkbenchActionSet):

    # 'WorkbenchActionSet' interface
#    enabled_for_perspectives = ['Experiments'] # The Ids of the perspectives that the action set is enabled in
#    visible_for_perspectives = ['BNF','Foo'] # The Ids of the perspectives that the action set is visible in
#    enabled_for_views = ['Red'] # The Ids of the views that the action set is enabled for
#    visible_for_views = ['Red'] # The Ids of the views that the action set is visible for
    
    # 'ActionSet' interface
    id = 'infobiotics.dashboard.plugins.simulator_results.action_set' # The action set's globally unique identifier

    menus = [
             
        # Experiment menu
        Menu(
            name='Results', path='MenuBar', after='Experiment',
#            groups=['McssGroup']
        ),
    ]

    tool_bars = [
        ToolBar(
            id='Results', 
#            groups=['McssGroup']
        ),
    ]
        
    actions = [
        
        # Experiment menu
        Action(
            path='MenuBar/Results', 
            name='Plotting',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.simulator_results.actions:SimulatorResultsAction',
        ),
        
        # Experiment toolbar
        Action(
            path='ToolBar/Results', 
            name='Plotting',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.simulator_results.actions:SimulatorResultsAction',
        ),
    ]

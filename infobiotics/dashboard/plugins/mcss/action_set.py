from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from actions import McssExperimentAction
            
class McssActionSet(WorkbenchActionSet):
    
    # 'WorkbenchActionSet' interface
#    enabled_for_perspectives = ['Experiments'] # The Ids of the perspectives that the action set is enabled in
#    visible_for_perspectives = ['BNF','Foo'] # The Ids of the perspectives that the action set is visible in
#    enabled_for_views = ['Red'] # The Ids of the views that the action set is enabled for
#    visible_for_views = ['Red'] # The Ids of the views that the action set is visible for

    # 'ActionSet' interface
    id = 'infobiotics.dashboard.plugins.mcss.action_set.McssActionSet' # The action set's globally unique identifier

    groups = [
        Group(id='UndoRedoGroup', path='MenuBar/Edit'),
#        Group(id='McssGroup', path='MenuBar/Experiment'),
    ]
        
    menus = [
             
        # Edit menu
        Menu(
            name='Edit', path='MenuBar', after='File', 
#            groups=['UndoRedoGroup']
        ),
        
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
        
        # Edit menu
        Action(path='MenuBar/Edit', name='Undo',  
          group='UndoRedoGroup',
          class_name='infobiotics.dashboard.plugins.mcss.actions:UndoAction'),
        Action(path='MenuBar/Edit', name='Redo',
          group='UndoRedoGroup',
          class_name='infobiotics.dashboard.plugins.mcss.actions:RedoAction'),
        
        # Experiment menu
        Action(path='MenuBar/Experiment', name='Simulation (mcss)',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
        
        # Experiment toolbar
        Action(path='ToolBar/Experiment', name='Simulation (mcss)',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
    ]

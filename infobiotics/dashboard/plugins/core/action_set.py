from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Action, Menu, ToolBar#, Group
            
class CoreActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.plugins.core.action_set.CoreActionSet'

    menus = [
#        Menu(
#            name='&Edit', 
#            path='MenuBar', 
#            after='File',
#        ),
        Menu(
            id='Experiments',
            name='E&xperiments', 
            path='MenuBar', 
            before='View',
        ),
    ]

    tool_bars = [
#        ToolBar(id='Edit'),
        ToolBar(id='Experiments'),
    ]

#    actions = [
#        Action(path='MenuBar/Edit', class_name='infobiotics.dashboard.plugins.core.actions.UndoAction'),
##        Action(path='ToolBar/Edit',  class_name='infobiotics.dashboard.plugins.core.actions.UndoAction'),
#
#        Action(path='MenuBar/Edit', class_name='infobiotics.dashboard.plugins.core.actions.RedoAction'),
##        Action(path='ToolBar/Edit',  class_name='infobiotics.dashboard.plugins.core.actions.RedoAction'),
#    ]
    
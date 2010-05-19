from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from actions import *


class BNFActionSet(WorkbenchActionSet):
    
    # 'WorkbenchActionSet' interface
#    enabled_for_perspectives = ['BNF'] # The Ids of the perspectives that the action set is enabled in
#    visible_for_perspectives = ['BNF'] # The Ids of the perspectives that the action set is visible in
#    enabled_for_views = ['Red'] # The Ids of the views that the action set is enabled for
#    visible_for_views = ['Red'] # The Ids of the views that the action set is visible for

    # 'ActionSet' interface
    id = 'infobiotics.bnf.bnf_action_set' # The action set's globally unique identifier
    
    tool_bars = [
#        ToolBar(name='BNF', id='bnf.bnf_tool_bar', path='ToolBar/BNF', groups=['TextFileGroup']),
    ]

    groups = [
        Group(
            id='BNFGroup',
            path='MenuBar/File',
            before="ExitGroup", 
            separator=False,
        ),
    ]

    menus = [
        Menu(
            name='&File',
            path='MenuBar',
        ),     
        Menu(
            name='&BNF',
            path='MenuBar',
            before='View',
        ),     
        Menu(
            name='&New',
            path='MenuBar/BNF',
        ),        
        Menu(
            name='&Open', 
            path='MenuBar/BNF',
        ),        
    ]
        
    actions = [
        
        # BNF/New menu        
        Action(path='MenuBar/BNF/New', name='LPP system',
            class_name='infobiotics.dashboard.plugins.bnf.actions:NewLPPAction'),
        Action(path='MenuBar/BNF/New', name='Stochastic P system',
            class_name='infobiotics.dashboard.plugins.bnf.actions:NewSPSAction'),
        Action(path='MenuBar/BNF/New', name='Lattice',
            class_name='infobiotics.dashboard.plugins.bnf.actions:NewLATAction'),
        Action(path='MenuBar/BNF/New', name='Module library',
            class_name='infobiotics.dashboard.plugins.bnf.actions:NewPLBAction'),

        # BNF/Open menu        
        Action(path='MenuBar/BNF/Open', name='LPP system',
            class_name='infobiotics.dashboard.plugins.bnf.actions:OpenLPPAction'),
        Action(path='MenuBar/BNF/Open', name='Stochastic P system',
            class_name='infobiotics.dashboard.plugins.bnf.actions:OpenSPSAction'),
        Action(path='MenuBar/BNF/Open', name='Lattice',
            class_name='infobiotics.dashboard.plugins.bnf.actions:OpenLATAction'),
        Action(path='MenuBar/BNF/Open', name='Module library',
            class_name='infobiotics.dashboard.plugins.bnf.actions:OpenPLBAction'),
        
        # File menu
        Action(path='MenuBar/File',
            group='BNFGroup',
            class_name='infobiotics.dashboard.plugins.bnf.actions:SaveAction'),
        Action(path='MenuBar/File',
            group='BNFGroup',
            class_name='infobiotics.dashboard.plugins.bnf.actions:SaveAsAction'),
        Action(path='MenuBar/File',
            group='BNFGroup',
            class_name='infobiotics.dashboard.plugins.bnf.actions:CloseAction'),
        Action(path='MenuBar/File',
            group='BNFGroup',
            class_name='infobiotics.dashboard.plugins.bnf.actions:CloseAllAction'),
        
#        Action(
#            path='ToolBar/BNF',
#            class_name='infobiotics.dashboard.plugins.bnf.actions:PrintSelectionAction',
##            group='file'
#        ),
    ]

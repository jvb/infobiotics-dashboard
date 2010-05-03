# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: action_set.py 405 2010-01-25 13:13:07Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/mcss/action_set.py $
# $Author: jvb $
# $Revision: 405 $
# $Date: 2010-01-25 13:13:07 +0000 (Mon, 25 Jan 2010) $


from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from actions import *
            
            
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
        
        #Edit menu
        Action(path='MenuBar/Edit', name='Undo',  
          group='UndoRedoGroup',
          class_name='infobiotics.dashboard.plugins.mcss.actions:UndoAction'),
        Action(path='MenuBar/Edit', name='Redo',
          group='UndoRedoGroup',
          class_name='infobiotics.dashboard.plugins.mcss.actions:RedoAction'),
        
        # Experiment menu
        Action(path='MenuBar/Experiment', name='mcss',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.mcss.actions:NewMcssExperimentAction'),
        
        # Experiment toolbar
        Action(path='ToolBar/Experiment', name='mcss',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.mcss.actions:NewMcssExperimentAction'),
#        Action(path='ToolBar/Experiment', name='Load mcss parameters',
#            group='McssGroup',
#            class_name='infobiotics.dashboard.plugins.mcss.actions:LoadMcssParametersAction'),
#        Action(path='ToolBar/Experiment', name='Save mcss parameters',
#            group='McssGroup',
#            class_name='infobiotics.dashboard.plugins.mcss.actions:SaveMcssParametersAction'),
    ]

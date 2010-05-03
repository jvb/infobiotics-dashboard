# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: pmodelchecker_action_set.py 383 2010-01-22 10:48:47Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/pmodelchecker/pmodelchecker_action_set.py $
# $Author: jvb $
# $Revision: 383 $
# $Date: 2010-01-22 10:48:47 +0000 (Fri, 22 Jan 2010) $


from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from actions import PRISMExperimentAction, MC2ExperimentAction
            
            
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
        Action(path='MenuBar/Experiment', name='PModelChecker (PRISM)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='MenuBar/Experiment', name='PModelChecker (MC2)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
#        Action(path='MenuBar/Experiment', name='PModelChecker',
#            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:'),
        
        # Experiment toolbar
#        Action(path='ToolBar/Experiment', name='PModelChecker',
#            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:NewPModelCheckerAction'),
        Action(path='ToolBar/Experiment', name='PModelChecker (PRISM)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:PRISMExperimentAction'),
        Action(path='ToolBar/Experiment', name='PModelChecker (MC2)',
            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:MC2ExperimentAction'),
#        Action(path='ToolBar/Experiment', name='PModelChecker',
#            class_name='infobiotics.dashboard.plugins.pmodelchecker.actions:'),
    ]

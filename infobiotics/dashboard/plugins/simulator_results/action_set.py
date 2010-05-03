# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: mcss_action_set.py 120 2009-12-08 14:48:20Z jvb $
# $HeadURL: svn+ssh://infobiotics.dyndns.org/svn/infobiotics/Infobiotics Dashboard/trunk/infobiotics/workbench/plugins/mcss/mcss_action_set.py $
# $Author: jvb $
# $Revision: 120 $
# $Date: 2009-12-08 14:48:20 +0000 (Tue, 08 Dec 2009) $


from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from actions import *
            
            
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
            name='SimulatorResults',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.simulator_results.actions:NewSimulatorResultsAction',
        ),
        
        # Experiment toolbar
        Action(
            path='ToolBar/Results', 
            name='SimulatorResults',
#            group='McssGroup',
            class_name='infobiotics.dashboard.plugins.simulator_results.actions:NewSimulatorResultsAction',
        ),
    ]

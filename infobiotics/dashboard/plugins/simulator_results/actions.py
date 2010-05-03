# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: actions.py 111 2009-12-03 17:11:22Z jvb $
# $HeadURL: svn+ssh://infobiotics.dyndns.org/svn/infobiotics/Infobiotics Dashboard/trunk/infobiotics/workbench/plugins/mcss/actions.py $
# $Author: jvb $
# $Revision: 111 $
# $Date: 2009-12-03 17:11:22 +0000 (Thu, 03 Dec 2009) $


from enthought.traits.ui.menu import UndoAction, RedoAction, RevertAction
from enthought.pyface.action.api import Action as PyFaceAction
from simulator_results import SimulationResultsDialog
from editor import SimulatorResultsEditor

class NewSimulatorResultsAction(PyFaceAction):
    ''' ...
     
    '''
    name = 'Simulator Results'
    tooltip = 'Plot simulation results'
    
    def perform(self, event=None):
        self.window.workbench.edit(
            obj=SimulationResultsDialog(),
            kind=SimulatorResultsEditor,
            use_existing=False
        )

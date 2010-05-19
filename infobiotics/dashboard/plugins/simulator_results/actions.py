from enthought.traits.ui.menu import UndoAction, RedoAction, RevertAction
from enthought.pyface.action.api import Action as PyFaceAction #TODO
from simulator_results import SimulationResultsDialog
from editor import SimulatorResultsEditor

class SimulatorResultsAction(PyFaceAction): #TODO
    name = 'Simulator Results'
    tooltip = 'Plot simulation results'
    
    def perform(self, event=None):
        self.window.workbench.edit(
            obj=SimulationResultsDialog(),
            kind=SimulatorResultsEditor,
            use_existing=False
        )

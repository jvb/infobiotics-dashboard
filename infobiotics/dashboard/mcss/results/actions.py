from enthought.traits.ui.menu import UndoAction, RedoAction, RevertAction
from enthought.pyface.action.api import Action as PyFaceAction #TODO
from simulator_results import SimulationResultsDialog
from editor import SimulatorResultsEditor

class SimulatorResultsAction(PyFaceAction): #TODO
    name = 'mcss'
    tooltip = 'Visualise mcss simulations.'
    
    def perform(self, event=None):
        obj = SimulationResultsDialog()
        if not obj.loaded:
            return
        self.window.workbench.edit(
            obj=obj,
            kind=SimulatorResultsEditor,
            use_existing=False
        )

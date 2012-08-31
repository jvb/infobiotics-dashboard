#from traitsui.menu import UndoAction, RedoAction, RevertAction
from pyface.action.api import Action as PyFaceAction #TODO
from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget
from editor import McssResultsEditor

class McssResultsAction(PyFaceAction): #TODO
    name = 'mcss'
    tooltip = 'Visualise mcss simulations.'
    
    def perform(self, event=None):
        obj = McssResultsWidget()
        obj.load()
        if not obj.loaded:
            # user cancelled load
            return
        self.window.workbench.edit(
            obj=obj,
            kind=McssResultsEditor,
            use_existing=False
        )

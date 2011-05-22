from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler
from infobiotics.core.views import ExperimentView
from enthought.pyface.api import GUI, error

class ExperimentHandler(ParamsHandler):
    
    def traits_view(self):
        return self.get_traits_view(ExperimentView)
    
    def perform(self, info):
        info.object.perform(thread=True)
        
    def _starting(self):
        self._progress_dialog_started = False
        self._progress_handler = ExperimentProgressHandler(model=self.model, title=self.title)
        
    def object__progress_percentage_changed(self, info):
        if info.object._interaction_mode == 'gui':
            if not self._progress_dialog_started:
                if info.object._progress_percentage > 0:
                    self._progress_dialog_started = True
                    self._progress_handler.edit_traits(kind='live', parent=info.ui.control) # must be live to receive progress updates
            # don't need to do anything else as self._progress_dialog should update 
            # based on changes to self.percentage

    def _finished(self, success):
        if self._progress_handler.info is not None and self._progress_handler.info.ui is not None:
            self._progress_handler.info.ui.dispose()
        if success:
            GUI.invoke_later(self.show_results) # essential
#        else: # done in Experiment._finished
#            GUI.invoke_later(error, None, "Experiment failed")
            
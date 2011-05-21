from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler
from infobiotics.core.views import ExperimentView
from enthought.pyface.timer.api import do_later

class ExperimentHandler(ParamsHandler):
    
    def traits_view(self):
        return self.get_traits_view(ExperimentView)
    
    def perform(self, info):
        info.object.perform(thread=True)
        
    def _starting(self):
        self._progress_dialog_started = False
        self._progress_handler = ExperimentProgressHandler(model=self.model)
        
    def object__progress_percentage_changed(self, info):
        if info.object._progress_percentage > 0:
            if not self._progress_dialog_started:
                self._progress_dialog_started = True
                self._progress_handler.edit_traits(kind='live', parent=info.ui.control) # must be live to receive progress updates
        # don't need to do anything else as self._progress_dialog should update 
        # based on changes to self.percentage

    def _finished(self, success):
        if self._progress_handler.info is not None and self._progress_handler.info.ui is not None:
            self._progress_handler.info.ui.dispose()
        if success:
            do_later(self.show_results)


if __name__ == '__main__':
    execfile('experiment.py')

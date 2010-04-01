from infobiotics.shared.api import Instance
from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler

class ExperimentHandler(ParamsHandler):
    
    _progress_handler = Instance(ExperimentProgressHandler)

    def __progress_handler_default(self):
        raise NotImplementedError

    def _show_progress(self):
        self._progress_handler.edit_traits(kind='live') # must be live to receive progress updates

    def perform(self, info):
        if info.object.perform(thread=True):
            self._show_progress()

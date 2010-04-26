from infobiotics.shared.api import Instance, Property, Bool
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

    has_valid_parameters = Property(Bool, depends_on='info.ui.errors')
    def _get_has_valid_parameters(self):
        # adapted from TraitsBackendQt/enthought/traits/ui/qt4/ui_base.py:BaseDialog._on_error() and ui_modal.py:_ModalDialog.init():ui.on_trait_change(self._on_error, 'errors', dispatch='ui') 
        return False if self.info.ui.errors > 0 else True
    
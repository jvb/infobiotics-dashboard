from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler
from infobiotics.core.views import ExperimentView
from enthought.traits.api import Instance, Property, Bool
import os.path

class ExperimentHandler(ParamsHandler):
    
    def traits_view(self):
        return self.get_traits_view(ExperimentView)
        
    _progress_handler = Instance(ExperimentProgressHandler)
    def __progress_handler_default(self):
        raise NotImplementedError('e.g. return McssExperimentProgressHandler(model=self.model)')

    def perform(self, info):
        ''' Hide window and show progress instead. '''
##        if self.close(info, True):
##            self._on_close(info)
        # if we do self._on_close(info) then subclasses can't catch events 
        # including 'finished'
        info.ui.control.setVisible(False) 
        if info.object.perform(thread=True):
            self._show_progress()

    def _show_progress(self):
        self._progress_handler.edit_traits(kind='live') # must be live to receive progress updates

    has_valid_parameters = Property(Bool, depends_on='info.ui.errors, model.executable')
    def _get_has_valid_parameters(self):
        # adapted from TraitsBackendQt/enthought/traits/ui/qt4/ui_base.py:BaseDialog._on_error() and ui_modal.py:_ModalDialog.init():ui.on_trait_change(self._on_error, 'errors', dispatch='ui') 
        if self.info.ui is None:
            return False
        if self.info.ui.errors > 0:
            return False
        elif not os.path.isfile(self.model.executable):
            return False
        return True
    
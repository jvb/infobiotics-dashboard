from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler
from infobiotics.core.views import ExperimentView
from enthought.pyface.api import GUI
import time

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
        self.model._thread.exit()
        if success:
            if not hasattr(self, '_imported_results_modules') or not self._imported_results_modules: # have we done the long import yet?
                # show 'Loading results message' (if first time, otherwise it will be fast)
                GUI.invoke_later(auto_close_message, message='Loading results', time=1, parent=self.info.ui.control)
                self._imported_results_modules = True
            time.sleep(0.5)
            GUI.invoke_later(self.show_results) # essential


# copied from enthought.traits.ui.message to tweak layout 

from enthought.pyface.timer.api import do_after
from enthought.traits.api import HasPrivateTraits, Str, Float
from enthought.traits.ui.api import View, HGroup, Item, spring

class AutoCloseMessage(HasPrivateTraits):
    message = Str('Please wait')
    time = Float(2.0) # The time (in seconds) to show the message

    def show(self, parent = None, title = ''):
        view = View(
            spring,
            HGroup(
                spring,
                Item('message',
                    show_label=False,
                    style='readonly',
                ),
                spring,
            ),
            spring,
            width=150,
            height=60,
            title=title,
        )
        do_after(
            int(1000.0 * self.time), 
            self.edit_traits(parent=parent, view=view).dispose
        )

def auto_close_message(message = 'Please wait', time=2.0, title='Please wait', parent=None):
    msg = AutoCloseMessage( message = message, time = time )
    msg.show( parent = parent, title = title )
            
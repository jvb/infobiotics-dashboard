from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler
from infobiotics.core.views import ExperimentView
from pyface.api import GUI
import time

class ExperimentHandler(ParamsHandler):
    
    def traits_view(self):
        return self.get_traits_view(ExperimentView)
    
    def perform(self, info):
        info.object.perform(thread=True)
        
    def _starting(self):
        self._progress_dialog_started = False
        self._progress_handler = ExperimentProgressHandler(model=self.model)
        
    def object__progress_percentage_changed(self, info):
        if info.object._interaction_mode == 'gui':
            if not self._progress_dialog_started:
                if info.object._progress_percentage > 0:
                    self._progress_dialog_started = True
                    self._progress_handler.edit_traits(
                        kind='live',
                        parent=info.ui.control,
#                        context={
#                            'object':self.model,
#                            'model':self.model,
#                            'controller':self._progress_handler,
#                            'handler':self
#                        },
                    ) # must be live to receive progress updates
            # don't need to do anything else as self._progress_dialog should update 
            # based on changes to self.percentage

    def _finished(self, success):
        if not hasattr(self, '_progress_handler') or self._progress_handler is None:
            return
        if self._progress_handler.info is not None and self._progress_handler.info.ui is not None:
            GUI.invoke_later(self._progress_handler.info.ui.dispose) # vital
        if hasattr(self.model, '_thread'):
            self.model._thread.exit()
        if success:
            if not hasattr(self, '_imported_results_modules') or not self._imported_results_modules: # have we done the long import yet?
                # show 'Loading results message' (if first time, otherwise it will be fast)
                GUI.invoke_later(auto_close_message, message='Loading results interface\n(only happens once)', time=1, parent=self.info.ui.control)
                self._imported_results_modules = True
            time.sleep(0.5)
            GUI.invoke_later(self.show_results) # essential


# copied from traitsui.message to tweak layout 

from pyface.timer.api import do_after
from traits.api import HasPrivateTraits, Str, Float
from traitsui.api import View, HGroup, Item, spring

class AutoCloseMessage(HasPrivateTraits):
    message = Str('Please wait')
    time = Float(2.0) # The time (in seconds) to show the message

    def show(self, parent=None, title='', width=200, height=80):
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
            width=width,
            height=height,
            title=title,
        )
        do_after(
            int(1000.0 * self.time),
            self.edit_traits(parent=parent, view=view).dispose
        )

def auto_close_message(message='Please wait', time=2.0, title='Please wait', parent=None):
    msg = AutoCloseMessage(message=message, time=time)
    msg.show(parent=parent, title=title)
            

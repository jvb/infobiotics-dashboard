from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler
from infobiotics.core.views import ExperimentView
from enthought.traits.api import Instance, Str, Button
from enthought.traits.ui.api import Controller, View, Item
from infobiotics.commons.traits.ui.qt4.progress_editor import ProgressEditor 

class ProgressDialog(Controller):
    
    def init(self, info):
        info.ui.title = self.model._handler.title
        self._closed = False
        
    title = Str
    
    def _title_default(self, info):
        return self.model.executable_name
    
    message = Str
    
    def _message_default(self, info):
        import os
        return os.path.split(self.model._params_file)[1]
    
    view = View(
        Item(
            '_progress_percentage',
            show_label=False,
            editor=ProgressEditor(
                title_name='title',
                message_name='handler.message',
                prefix_message=True,
                min=0,
                max=100,
#                show_text=False,
                show_percent=True,
                show_time=True,
                show_max=True,
                show_value=True,
            ),
        ),
        buttons=['Cancel'],
        close_result=False, # make 'x' behave like cancel: http://markmail.org/message/5ykjtwa3xdrvg45w
        resizable=True,
        width=250,
    )
    
    def close(self, info, is_ok):
        if not is_ok:
            from enthought.traits.ui.message import error
            return error(title='Confirm cancellation', message='Do you really want to cancel the experiment?', parent=self.info.ui.control)
        return is_ok
    
    def closed(self, info, is_ok):
        self._closed = True
        if not is_ok:
            if self.model._child.isalive():
                self.model._child.terminate(force=True)
        return super(ProgressDialog, self).closed(info, is_ok)
            
            
class ExperimentHandler(ParamsHandler):
    
    def traits_view(self):
        return self.get_traits_view(ExperimentView)

    def perform(self, info):
#        info.ui.control.setVisible(False) 
        info.object.perform(thread=True)
        
    def _starting(self):
        self._progress_dialog = ProgressDialog(model=self.model)
        self._progress_dialog_started = False

    def object_message_changed(self, info):
        if info.initialized:
            if hasattr(self, '_progress_dialog'):
                self._progress_dialog.message = self.model.message

    def object__progress_percentage_changed(self, info):
        if info.initialized:
            if hasattr(self, '_progress_dialog') and self._progress_dialog is not None and not self._progress_dialog_started:
                self._progress_dialog_started = True
                self._progress_dialog.edit_traits(
                    kind='live', # must be live to receive progress updates
                    parent=self.info.ui.control,
                ) 
            # do nothing, self._progress_dialog should update based on self._progress_percentage
    
    def _finished(self, success):
        if hasattr(self, '_progress_dialog') and not self._progress_dialog._closed:
            # must call close with correct info (i.e. not self.info)
            if self._progress_dialog.close(self._progress_dialog.info, True):
                self._progress_dialog._on_close(self._progress_dialog.info)
#        if success:
#            self.show_results()
        
    def show_results(self):
        raise NotImplementedError

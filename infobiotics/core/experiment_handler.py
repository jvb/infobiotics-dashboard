from params_handler import ParamsHandler
from experiment_progress_handler import ExperimentProgressHandler
from infobiotics.core.views import ExperimentView
from enthought.traits.api import Instance

class ExperimentHandler(ParamsHandler):
    
    def traits_view(self):
        return self.get_traits_view(ExperimentView)
        
    def _starting(self):
        pass #TODO create and show *cancellable* progress dialog
        self._progress_dialog_started = False

    def object__progress_percentage_changed(self, info):
        if not self._progress_dialog_started:
            self._progress_dialog_started = True
#            self._progress_dialog.edit_traits(kind='live') # must be live to receive progress updates
#        print self.info.object._progress_percentage
        pass #TODO nothing, self._progress_dialog should update based on self.percentage
    
    def _finished(self, success):
        #TODO close progress dialog
        if success:
            print 'got here'
#            self.show_results()

    def perform(self, info):
        ''' Hide window and show progress instead. '''
##        if self.close(info, True):
##            self._on_close(info)
        # if we do self._on_close(info) then subclasses can't catch events 
        # including 'finished'
#        info.ui.control.setVisible(False) 
        info.object.perform(thread=True)

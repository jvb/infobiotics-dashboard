from infobiotics.mcss.api import McssParamsHandler, McssExperimentProgressHandler
from infobiotics.core.experiment_handler import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def _starting(self):
        pass #TODO create and show *cancellable* progress dialog
        self._progress_dialog_started = False

    def object__progress_percentage_changed(self, info):
        if not self._progress_dialog_started:
            self._progress_dialog_started = True
#            self._progress_dialog.edit_traits()
        print self.info.object._progress_percentage
        pass #TODO nothing, self._progress_dialog should update based on self.percentage
    
    def _finished(self, success):
        #TODO close progress dialog
        if success:
            print 'got here'
#            self.show_results()

    def show_results(self):
        import os.path
        if os.path.exists(self.model.data_file_):
            from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
            w = SimulationResultsDialog(filename=self.model.data_file_)
            from infobiotics.commons.qt4 import centre_window
            centre_window(w)
            w.show()
        else:
            print "Results file '%s' does not exist, plotting aborted." % self.model.data_file_


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    

from infobiotics.common.api import ExperimentHandler

class PModelCheckerExperimentHandler(ExperimentHandler):

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
#        self._progress_handler.message = 'Loading results...' # doesn't change the message!
        self.show_results()

    def show_results(self):
        import os.path
        if os.path.exists(self.model.results_file):
#            from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
#            w = SimulationResultsDialog(filename=self.model.data_file_)
#            from infobiotics.commons.qt4 import centre_window
#            centre_window(w)
#            w.show()
#            from infobiotics.pmodelchecker.results.pmodelchecker_results_matplotlib import TraitedPrismResultsPlotter
            from infobiotics.pmodelchecker.results.pmodelchecker_results_mayavi import TraitedPrismResultsPlotter
        else:
            print 'never been here before'
            from enthought.traits.ui.message import auto_close_message
            auto_close_message(self.child.before)
            
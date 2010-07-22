from infobiotics.common.api import ExperimentHandler
import os.path

class PModelCheckerExperimentHandler(ExperimentHandler):

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
#        self._progress_handler.message = 'Loading results...' # doesn't change the message!
        self.show_results()

    def show_results(self):
        if os.path.exists(self.model.results_file_):
#            from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
#            w = SimulationResultsDialog(filename=self.model.data_file_)
#            from infobiotics.commons.qt4 import centre_window
#            centre_window(w)
#            w.show()
#            from infobiotics.pmodelchecker.results.pmodelchecker_results_matplotlib import TraitedPrismResultsPlotter
            from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
            PModelCheckerResults(self.model.results_file_).configure_traits()
        else:
            print 'never been here before'
            from enthought.traits.ui.message import auto_close_message
            auto_close_message(self.child.before)


if __name__ == '__main__':
    from prism.prism_experiment import PRISMExperiment
    PRISMExperiment('../../tests/workbench_examples/motifs/NAR/pmodelchecker_example/NAR_PRISM.params').configure()
                
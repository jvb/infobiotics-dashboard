from infobiotics.common.api import ExperimentHandler
import os.path
from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults

class PModelCheckerExperimentHandler(ExperimentHandler):

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
#        self._progress_handler.message = 'Loading results...' # doesn't change the message!
        self.show_results()

    def show_results(self):
        if os.path.exists(self.model.results_file_):
            PModelCheckerResults(self.model.results_file_).configure_traits()
        else:
            print 'never been here before' #TODO remove
            from enthought.traits.ui.message import auto_close_message
            auto_close_message(self.child.before)


if __name__ == '__main__':
    from prism.prism_experiment import PRISMExperiment
    PRISMExperiment('../../tests/workbench_examples/motifs/NAR/pmodelchecker_example/NAR_PRISM.params').configure()
                
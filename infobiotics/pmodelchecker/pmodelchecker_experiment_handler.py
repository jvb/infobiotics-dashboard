from infobiotics.core.experiment_handler import ExperimentHandler
import os.path
from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults

class PModelCheckerExperimentHandler(ExperimentHandler):

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
#        self._progress_handler.message = 'Loading results...' #TODO does this do anything?
#        if self.model.session.interactive: #TODO
        if self.model.task in ('Approximate','Verify'):
            self.show_results()

    def show_results(self):
        if os.path.exists(self.model.results_file_):
            PModelCheckerResults(self.model.results_file_).configure()
        else:
            print "Results file '%s' does not exist, plotting aborted." % self.model.results_file_


if __name__ == '__main__':
    from prism.prism_experiment import PRISMExperiment
    PRISMExperiment('../../tests/workbench_examples/motifs/NAR/pmodelchecker_example/NAR_PRISM.params').configure()
                
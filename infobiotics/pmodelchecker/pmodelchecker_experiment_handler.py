from infobiotics.core.experiment_handler import ExperimentHandler
import os.path
from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults

class PModelCheckerExperimentHandler(ExperimentHandler):

    def show_results(self):
#        if self.model.task in ('Approximate', 'Verify'): # PRISM only?
        if os.path.exists(self.model.results_file_):
            PModelCheckerResults(self.model.results_file_).configure()
        else:
            print "Results file '%s' does not exist, plotting aborted." % self.model.results_file_


if __name__ == '__main__':
    from prism.prism_experiment import PRISMExperiment
    PRISMExperiment('../../tests/workbench_examples/motifs/NAR/pmodelchecker_example/NAR_PRISM.params').configure()
                

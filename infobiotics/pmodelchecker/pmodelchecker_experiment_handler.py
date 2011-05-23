from infobiotics.core.experiment_handler import ExperimentHandler
import os.path
from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults

class PModelCheckerExperimentHandler(ExperimentHandler):

    def show_results(self):
        if hasattr(self.model, 'results_file_') and os.path.exists(self.model.results_file_):
            PModelCheckerResults(self.model.results_file_).configure()
        else:
            print "Results file '%s' does not exist, plotting aborted." % self.model.results_file

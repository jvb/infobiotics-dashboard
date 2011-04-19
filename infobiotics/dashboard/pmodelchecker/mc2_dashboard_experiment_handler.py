from infobiotics.pmodelchecker.mc2.mc2_experiment import MC2ExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler
import commons

class MC2DashboardExperimentHandler(MC2ExperimentHandler, DashboardExperimentHandler):

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. '''
        commons.edit_pmodelchecker_results_file(
            file=self.model.results_file_,
#            application=self.application,
        )

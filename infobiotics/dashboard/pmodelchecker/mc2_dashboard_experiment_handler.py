from infobiotics.pmodelchecker.mc2.mc2_experiment import MC2ExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler
import commons

class MC2DashboardExperimentHandler(MC2ExperimentHandler, DashboardExperimentHandler):

    def show_results(self): # called by ExperimentHandler._finished
        commons.edit_pmodelchecker_results_file(
            self.model.results_file_,
            self.application
        )

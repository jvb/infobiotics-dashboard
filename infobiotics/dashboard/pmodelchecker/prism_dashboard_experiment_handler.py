from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler
import commons

class PRISMDashboardExperimentHandler(PRISMExperimentHandler, DashboardExperimentHandler):

    def show_results(self): # called by ExperimentHandler._finished
        commons.edit_pmodelchecker_results_file(
            self.model.results_file_,
            self.application
        )

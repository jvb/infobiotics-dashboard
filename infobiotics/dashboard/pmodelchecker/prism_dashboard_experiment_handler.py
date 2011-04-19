from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler
import commons

class PRISMDashboardExperimentHandler(PRISMExperimentHandler, DashboardExperimentHandler):

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. ''' #TODO?
        commons.edit_pmodelchecker_results_file(
            file=self.model.results_file_,
#            application=self.application,
        )

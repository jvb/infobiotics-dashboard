from infobiotics.pmodelchecker.prism.api import PRISMExperimentHandler
from infobiotics.dashboard.core.api import DashboardExperimentHandler
from infobiotics.dashboard.pmodelchecker.api import PRISMDashboardExperimentProgressHandler
import commons

class PRISMDashboardExperimentHandler(PRISMExperimentHandler, DashboardExperimentHandler):

    def __progress_handler_default(self):
        return PRISMDashboardExperimentProgressHandler(model=self.model, application=self.application)

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. ''' #TODO?
        commons.edit_pmodelchecker_results_file(
            file=self.model.results_file_,
#            application=self.application,
        )

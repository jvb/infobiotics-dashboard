from infobiotics.pmodelchecker.mc2.api import MC2ExperimentHandler
from infobiotics.dashboard.core.api import DashboardExperimentHandler
from infobiotics.dashboard.pmodelchecker.api import MC2DashboardExperimentProgressHandler
import commons

class MC2DashboardExperimentHandler(MC2ExperimentHandler, DashboardExperimentHandler):

    def __progress_handler_default(self):
        return MC2DashboardExperimentProgressHandler(model=self.model, application=self.application)

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. '''
        commons.edit_pmodelchecker_results_file(
            file=self.model.results_file_,
#            application=self.application,
        )

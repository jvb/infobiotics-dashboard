from infobiotics.pmodelchecker.prism.api import PRISMExperimentHandler
from infobiotics.dashboard.pmodelchecker.api import PRISMDashboardExperimentProgressHandler
from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
from infobiotics.dashboard.plugins.pmodelchecker.editor import PModelCheckerResultsEditor
from infobiotics.dashboard.core.api import DashboardExperimentHandler

class PRISMDashboardExperimentHandler(PRISMExperimentHandler, DashboardExperimentHandler):

    def __progress_handler_default(self):
        return PRISMDashboardExperimentProgressHandler(model=self.model, application=self.application)

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. ''' #TODO?
        self.application.workbench.edit(
            obj=PModelCheckerResults(file_name=self.model.results_file_),
            kind=PModelCheckerResultsEditor,
            use_existing=False,
        )

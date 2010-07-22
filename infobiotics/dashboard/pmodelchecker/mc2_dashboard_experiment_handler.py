from infobiotics.pmodelchecker.mc2.api import MC2ExperimentHandler
from infobiotics.dashboard.pmodelchecker.api import MC2DashboardExperimentProgressHandler
from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
from infobiotics.dashboard.plugins.pmodelchecker.editor import PModelCheckerResultsEditor
from infobiotics.dashboard.core.api import DashboardExperimentHandler

class MC2DashboardExperimentHandler(MC2ExperimentHandler, DashboardExperimentHandler):

    def __progress_handler_default(self):
        return MC2DashboardExperimentProgressHandler(model=self.model, application=self.application)

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. '''
        self.application.workbench.edit(
            obj=PModelCheckerResults(file_name=self.model.results_file_),
            kind=PModelCheckerResultsEditor,
            use_existing=False,
        )

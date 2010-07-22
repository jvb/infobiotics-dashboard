from infobiotics.pmodelchecker.prism.api import PRISMExperimentHandler
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.pmodelchecker.api import PRISMDashboardExperimentProgressHandler

class PRISMDashboardExperimentHandler(PRISMExperimentHandler):

    application = Instance(InfobioticsDashboardWorkbenchApplication)

    def __progress_handler_default(self):
        return PRISMDashboardExperimentProgressHandler(model=self.model, application=self.application)

    def _show_progress(self):
        #TODO maybe raise experiments queue view here (moved to new class DashboardExperimentHandler)
        super(PRISMDashboardExperimentHandler, self)._show_progress()

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. ''' #TODO?
        from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
        from infobiotics.dashboard.plugins.pmodelchecker.editor import PModelCheckerResultsResultsEditor #TODO editors
        self.application.workbench.edit(
            obj=PModelCheckerResults(file_name=self.model.results_file_),
            kind=PModelCheckerResultsResultsEditor,
            use_existing=False,
        )

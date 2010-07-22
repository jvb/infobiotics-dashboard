from infobiotics.pmodelchecker.mc2.api import MC2ExperimentHandler
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.pmodelchecker.api import MC2DashboardExperimentProgressHandler

class MC2DashboardExperimentHandler(MC2ExperimentHandler):

    application = Instance(InfobioticsDashboardWorkbenchApplication)

    def __progress_handler_default(self):
        return MC2DashboardExperimentProgressHandler(model=self.model, application=self.application)

    def _show_progress(self):
        #TODO maybe raise experiments queue view here (moved to new class DashboardExperimentHandler)
        super(MC2DashboardExperimentHandler, self)._show_progress()

    def show_results(self):
        ''' Called by PModelCheckerExperimentHandler.object_finished_changed. ''' #TODO?
        from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
        from infobiotics.dashboard.plugins.pmodelchecker.editor import PModelCheckerResultsResultsEditor #TODO editors
        self.application.workbench.edit(
            obj=PModelCheckerResults(file_name=self.model.results_file_),
            kind=PModelCheckerResultsResultsEditor,
            use_existing=False,
        )

from infobiotics.mcss.api import McssExperimentHandler
from infobiotics.dashboard.mcss.api import McssDashboardExperimentProgressHandler
from infobiotics.dashboard.core.api import DashboardExperimentHandler

class McssDashboardExperimentHandler(McssExperimentHandler, DashboardExperimentHandler):

    def __progress_handler_default(self):
        return McssDashboardExperimentProgressHandler(model=self.model, application=self.application)

    def show_results(self):
        ''' Called by McssExperimentHandler.object_finished_changed '''
        from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog
        from infobiotics.dashboard.plugins.simulator_results.editor import SimulatorResultsEditor
        self.application.workbench.edit(
            obj=SimulationResultsDialog(filename=self.model.data_file_),
            kind=SimulatorResultsEditor,
            use_existing=False,
        )
        
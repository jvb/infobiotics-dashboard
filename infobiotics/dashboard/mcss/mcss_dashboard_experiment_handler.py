from infobiotics.mcss.api import McssExperimentHandler
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.mcss.api import McssDashboardExperimentProgressHandler

class McssDashboardExperimentHandler(McssExperimentHandler):#, DashboardExperimentHandler): #TODO what would/could/should this do?

    application = Instance(InfobioticsDashboardWorkbenchApplication)

    def __progress_handler_default(self):
        return McssDashboardExperimentProgressHandler(model=self.model, application=self.application)

    def _show_progress(self):
        #TODO maybe raise experiments queue view here (moved to new class DashboardExperimentHandler)
        super(McssDashboardExperimentHandler, self)._show_progress()

    def show_results(self):
        ''' Called by McssExperimentHandler.object_finished_changed '''
        from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog
        from infobiotics.dashboard.plugins.simulator_results.editor import SimulatorResultsEditor
        self.application.workbench.edit(
            obj=SimulationResultsDialog(filename=self.model.data_file_),
            kind=SimulatorResultsEditor,
            use_existing=False,
        )
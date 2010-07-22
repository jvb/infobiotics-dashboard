from infobiotics.poptimizer.api import POptimizerExperimentHandler
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.poptimizer.api import POptimizerDashboardExperimentProgressHandler

class POptimizerDashboardExperimentHandler(POptimizerExperimentHandler):#, DashboardExperimentHandler): #TODO what would/could/should this do?

    application = Instance(InfobioticsDashboardWorkbenchApplication)

    def __progress_handler_default(self):
        return POptimizerDashboardExperimentProgressHandler(model=self.model, application=self.application)

    def _show_progress(self):
        #TODO maybe raise experiments queue view here (moved to new class DashboardExperimentHandler)
        super(POptimizerDashboardExperimentHandler, self)._show_progress()

    def show_results(self):
        ''' Called by POptimizerExperimentHandler.object_finished_changed '''
#        from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog
#        from infobiotics.dashboard.plugins.simulator_results.editor import SimulatorResultsEditor
#        self.application.workbench.edit(
#            obj=SimulationResultsDialog(filename=self.model.data_file_),
#            kind=SimulatorResultsEditor,
#            use_existing=False,
#        )
        print 'POptimizerDashboardExperimentHandler.show_results'
        
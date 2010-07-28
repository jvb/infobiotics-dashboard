from infobiotics.poptimizer.api import POptimizerExperimentHandler
from infobiotics.dashboard.poptimizer.api import POptimizerDashboardExperimentProgressHandler
from infobiotics.dashboard.core.api import DashboardExperimentHandler

class POptimizerDashboardExperimentHandler(POptimizerExperimentHandler, DashboardExperimentHandler):

    def __progress_handler_default(self):
        return POptimizerDashboardExperimentProgressHandler(model=self.model, application=self.application)

#    def show_results(self):
#        ''' Called by POptimizerExperimentHandler.object_finished_changed '''
##        from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog
##        from infobiotics.dashboard.plugins.simulator_results.editor import SimulatorResultsEditor
##        self.application.workbench.edit(
##            obj=SimulationResultsDialog(filename=self.model.data_file_),
##            kind=SimulatorResultsEditor,
##            use_existing=False,
##        )
#        print 'POptimizerDashboardExperimentHandler.show_results'
        
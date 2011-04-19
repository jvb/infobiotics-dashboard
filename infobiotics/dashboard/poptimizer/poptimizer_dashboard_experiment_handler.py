from infobiotics.poptimizer.api import POptimizerExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler

class POptimizerDashboardExperimentHandler(POptimizerExperimentHandler, DashboardExperimentHandler):
    pass
    #TODO show_results
#    def show_results(self):
#        ''' Called by POptimizerExperimentHandler.object_finished_changed '''
##        from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget
##        from infobiotics.dashboard.mcss.results.editor import McssResultsEditor
##        self.application.workbench.edit(
##            obj=McssResultsWidget(filename=self.model.data_file_),
##            kind=McssResultsEditor,
##            use_existing=False,
##        )
#        print 'POptimizerDashboardExperimentHandler.show_results'

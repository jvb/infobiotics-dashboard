from infobiotics.mcss.mcss_experiment_handler import McssExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler

class McssDashboardExperimentHandler(McssExperimentHandler, DashboardExperimentHandler):

    def show_results(self):
        ''' Called by McssExperimentHandler.object_finished_changed '''
        from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget
        from infobiotics.dashboard.mcss.results.editor import McssResultsEditor
        self.application.workbench.edit(
            obj=McssResultsWidget(filename=self.model.data_file_),
            kind=McssResultsEditor,
            use_existing=False,
        )
        

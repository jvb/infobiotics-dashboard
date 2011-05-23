from infobiotics.poptimizer.api import POptimizerExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler

class POptimizerDashboardExperimentHandler(DashboardExperimentHandler, POptimizerExperimentHandler):

    def show_results(self):
        ''' Called by POptimizerExperimentHandler.object_finished_changed '''
        self.application.workbench.edit(
            obj=self.model,
            kind=POptimizerResultsEditor,
            use_existing=False,
        )


from infobiotics.dashboard.core.dashboard_experiment_editor import DashboardExperimentEditor
from infobiotics.poptimizer.poptimizer_results import POptimizerResults

class POptimizerResultsEditor(DashboardExperimentEditor):
    def create_ui(self, parent):
        return POptimizerResults(experiment=self.obj).edit_traits(kind='panel', parent=parent)

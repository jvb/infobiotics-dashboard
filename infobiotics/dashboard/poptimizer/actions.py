from pyface.action.api import Action
from infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment import POptimizerDashboardExperiment

class POptimizerExperimentAction(Action):
#    name = 'POptimizer'
    name = 'Optimisation'
    tooltip = 'Optimise the structure and parameters and of a model.'
    def perform(self, event=None):
        obj = POptimizerDashboardExperiment(application=self.window.workbench.application)
        from infobiotics.dashboard.core.dashboard_experiment_editor import DashboardExperimentEditor
        self.window.workbench.edit(
            obj=obj,
            kind=DashboardExperimentEditor,
            use_existing=False
        )
#        obj.edit()
    
#        # testing POptimizerDashboardExperimentHandler.show_results()
#        obj._handler.show_results()

from enthought.pyface.action.api import Action
from infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment import POptimizerDashboardExperiment
#from infobiotics.dashboard.plugins.experiments.params_experiment_editor import ParamsExperimentEditor

class POptimizerExperimentAction(Action):
#    name = 'POptimizer'
    name = 'Optimisation'
    tooltip = 'Optimise the structure and parameters and of a model.'
    def perform(self, event=None):
        obj = POptimizerDashboardExperiment(application=self.window.workbench.application)
#        self.window.workbench.edit(
#            obj=obj,
#            kind=ParamsExperimentEditor,
#            use_existing=False
#        )
        obj.edit()

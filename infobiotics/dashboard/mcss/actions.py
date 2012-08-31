from enthought.pyface.action.api import Action
from infobiotics.dashboard.mcss.mcss_dashboard_experiment import McssDashboardExperiment

class McssExperimentAction(Action):
#    name = 'mcss'
    name = 'Simulation'
    tooltip = 'Multi-compartmental stochastic simulation of a model.'
    
    def perform(self, event=None):
        obj = McssDashboardExperiment(application=self.window.workbench.application)
        from infobiotics.dashboard.core.dashboard_experiment_editor import DashboardExperimentEditor
        self.window.workbench.edit(
            obj=obj,
            kind=DashboardExperimentEditor,
            use_existing=False
        )
#        obj.edit()
        

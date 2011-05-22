from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperiment
from infobiotics.dashboard.core.dashboard_experiment import DashboardExperiment
from infobiotics.dashboard.pmodelchecker.prism_dashboard_experiment_handler import PRISMDashboardExperimentHandler 

class PRISMDashboardExperiment(DashboardExperiment, PRISMExperiment):
    
    def __handler_default(self):
        return PRISMDashboardExperimentHandler(model=self, application=self.application)

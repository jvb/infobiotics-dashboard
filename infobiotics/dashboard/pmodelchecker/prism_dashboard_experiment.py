from infobiotics.api import PRISMExperiment
from infobiotics.dashboard.core.api import DashboardExperiment
from infobiotics.dashboard.pmodelchecker.api import PRISMDashboardExperimentHandler 

class PRISMDashboardExperiment(PRISMExperiment, DashboardExperiment):
    
    def _handler_default(self):
        return PRISMDashboardExperimentHandler(model=self, application=self.application)

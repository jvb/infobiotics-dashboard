from infobiotics.api import POptimizerExperiment
from infobiotics.dashboard.core.api import DashboardExperiment 
from infobiotics.dashboard.poptimizer.api import POptimizerDashboardExperimentHandler 

class POptimizerDashboardExperiment(POptimizerExperiment, DashboardExperiment):
    
    def _handler_default(self):
        return POptimizerDashboardExperimentHandler(model=self, application=self.application)

from infobiotics.poptimizer.poptimizer_experiment import POptimizerExperiment
from infobiotics.dashboard.core.dashboard_experiment import DashboardExperiment 
from infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment_handler import POptimizerDashboardExperimentHandler 

class POptimizerDashboardExperiment(POptimizerExperiment, DashboardExperiment):
    
    def _handler_default(self):
        return POptimizerDashboardExperimentHandler(model=self, application=self.application)

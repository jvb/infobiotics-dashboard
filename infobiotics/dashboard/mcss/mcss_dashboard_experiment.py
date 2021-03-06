from infobiotics.mcss.mcss_experiment import McssExperiment
from infobiotics.dashboard.core.dashboard_experiment import DashboardExperiment
from infobiotics.dashboard.mcss.mcss_dashboard_experiment_handler import McssDashboardExperimentHandler 

class McssDashboardExperiment(DashboardExperiment, McssExperiment):
    
    def __handler_default(self):
        return McssDashboardExperimentHandler(model=self, application=self.application)

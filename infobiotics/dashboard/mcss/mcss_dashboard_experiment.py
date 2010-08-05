from infobiotics.api import McssExperiment
from infobiotics.dashboard.core.api import DashboardExperiment
from infobiotics.dashboard.mcss.api import McssDashboardExperimentHandler 

class McssDashboardExperiment(McssExperiment, DashboardExperiment):
    
    def _handler_default(self):
        return McssDashboardExperimentHandler(model=self, application=self.application)

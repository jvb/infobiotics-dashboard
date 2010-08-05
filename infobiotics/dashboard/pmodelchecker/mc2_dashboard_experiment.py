from infobiotics.api import MC2Experiment
from infobiotics.dashboard.core.api import DashboardExperiment 
from infobiotics.dashboard.pmodelchecker.api import MC2DashboardExperimentHandler 

class MC2DashboardExperiment(MC2Experiment, DashboardExperiment):
    
    def _handler_default(self):
        return MC2DashboardExperimentHandler(model=self, application=self.application)

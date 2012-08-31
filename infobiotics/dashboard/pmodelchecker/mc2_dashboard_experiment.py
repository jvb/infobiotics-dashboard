from infobiotics.pmodelchecker.mc2.mc2_experiment import MC2Experiment
from infobiotics.dashboard.core.dashboard_experiment import DashboardExperiment 
from infobiotics.dashboard.pmodelchecker.mc2_dashboard_experiment_handler import MC2DashboardExperimentHandler 

class MC2DashboardExperiment(DashboardExperiment, MC2Experiment):
    
    def __handler_default(self):
        return MC2DashboardExperimentHandler(model=self, application=self.application)

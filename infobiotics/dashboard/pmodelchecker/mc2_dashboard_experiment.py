from infobiotics.api import MC2Experiment
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.pmodelchecker.api import MC2DashboardExperimentHandler 

class MC2DashboardExperiment(MC2Experiment):
    
    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
    def _handler_default(self):
        return MC2DashboardExperimentHandler(model=self, application=self.application)

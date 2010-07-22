from infobiotics.api import PRISMExperiment
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.pmodelchecker.api import PRISMDashboardExperimentHandler 

class PRISMDashboardExperiment(PRISMExperiment):
    
    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
    def _handler_default(self):
        return PRISMDashboardExperimentHandler(model=self, application=self.application)

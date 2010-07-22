from infobiotics.api import POptimizerExperiment
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.poptimizer.api import POptimizerDashboardExperimentHandler 

class POptimizerDashboardExperiment(POptimizerExperiment):
    
    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
    def _handler_default(self):
        return POptimizerDashboardExperimentHandler(model=self, application=self.application)

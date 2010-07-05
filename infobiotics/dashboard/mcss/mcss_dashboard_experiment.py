from infobiotics.api import McssExperiment
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.mcss.api import McssDashboardExperimentHandler 

class McssDashboardExperiment(McssExperiment):
    
    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
    def _get_handler(self):
        return McssDashboardExperimentHandler(model=self, application=self.application)

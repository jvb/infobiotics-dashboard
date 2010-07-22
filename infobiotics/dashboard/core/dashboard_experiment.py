from enthought.traits.api import HasTraits, Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class DashboardExperiment(HasTraits):
    
    application = Instance(InfobioticsDashboardWorkbenchApplication)

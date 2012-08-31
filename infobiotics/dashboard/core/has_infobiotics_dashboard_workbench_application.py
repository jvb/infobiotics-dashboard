from enthought.traits.api import HasTraits, Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class HasInfobioticsDashboardWorkbenchApplication(HasTraits):
    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
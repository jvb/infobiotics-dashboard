from enthought.traits.api import HasTraits, Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class DashboardExperimentProgressHandler(HasTraits):

    application = Instance(InfobioticsDashboardWorkbenchApplication)

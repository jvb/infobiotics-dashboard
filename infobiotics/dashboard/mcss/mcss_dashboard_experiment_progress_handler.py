from infobiotics.mcss.api import McssExperimentProgressHandler
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class McssDashboardExperimentProgressHandler(McssExperimentProgressHandler):

    application = Instance(InfobioticsDashboardWorkbenchApplication)

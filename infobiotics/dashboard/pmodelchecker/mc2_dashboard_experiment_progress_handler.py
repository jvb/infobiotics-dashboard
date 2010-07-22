from infobiotics.pmodelchecker.mc2.api import MC2ExperimentProgressHandler    
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class MC2DashboardExperimentProgressHandler(MC2ExperimentProgressHandler):

    application = Instance(InfobioticsDashboardWorkbenchApplication)

from infobiotics.pmodelchecker.prism.api import PRISMExperimentProgressHandler    
from enthought.traits.api import Instance
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class PRISMDashboardExperimentProgressHandler(PRISMExperimentProgressHandler):

    application = Instance(InfobioticsDashboardWorkbenchApplication)

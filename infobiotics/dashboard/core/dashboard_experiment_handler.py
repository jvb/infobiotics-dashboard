from enthought.traits.api import HasTraits, Instance, on_trait_change
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class DashboardExperimentHandler(HasTraits):

    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
    @on_trait_change('application:exiting')
    def close_on_exit(self): 
        self._on_close(self.info)

#    def _show_progress(self):
#        #TODO maybe raise experiments queue view here (moved to new class DashboardExperimentHandler)
#        super(PRISMDashboardExperimentHandler, self)._show_progress()

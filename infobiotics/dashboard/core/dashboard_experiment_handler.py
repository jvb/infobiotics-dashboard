from enthought.traits.api import HasTraits, Instance, on_trait_change
from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication

class DashboardExperimentHandler(HasTraits):

    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
    @on_trait_change('application:stopped')
    def close_on_exit(self, event): 
        self._on_close(self.info)#self.close_window(self.info) # equivalent because application ends event loop
         
#    def _show_progress(self):
#        #TODO maybe raise experiments queue view here (moved to new class DashboardExperimentHandler)
#        super(PRISMDashboardExperimentHandler, self)._show_progress()

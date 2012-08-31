from has_infobiotics_dashboard_workbench_application import HasInfobioticsDashboardWorkbenchApplication
from traits.api import on_trait_change

class DashboardExperimentHandler(HasInfobioticsDashboardWorkbenchApplication):

    _imported_results_modules = True 

    @on_trait_change('application:stopped')
    def close_on_exit(self, event):
        if self.info.ui is not None: # guard against window have already been closed
            self._on_close(self.info)#self.close_window(self.info) # equivalent because application ends event loop
         
#    def _show_progress(self):
#        #TODO maybe raise experiments queue view here (moved to new class DashboardExperimentHandler)
#        super(PRISMDashboardExperimentHandler, self)._show_progress()

#    def perform(self, info):
#        print 'DashboardExperimentHandler'
#        info.object.perform(thread=True)

class DashboardParamsExperimentHandler(ParamsExperimentHandler, DashboardParamsHandler):
    
#    def load(self, info):
#        pass

#    def perform(self, info):
#        pass

    # react to experiment (expect) traits changes
    def model_overall_progress_changed(self):
        pass
        
    cancel = Event
    
    def _cancel_fired(self):
        pass

#    traits_view = pass
from has_infobiotics_dashboard_workbench_application import HasInfobioticsDashboardWorkbenchApplication
from enthought.traits.api import Str 

class DashboardExperiment(HasInfobioticsDashboardWorkbenchApplication):
    
    _interaction_mode = Str('gui') # overrides _interaction_mode in Params but means that DashboardExperiment must be imported before McssDashboardExperiment for example 

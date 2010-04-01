#from infobiotics.dashboard.params.params_experiment_controller import ParamsExperimentController
#class McssParamsExperimentController(ParamsExperimentController, McssParamsController):

from infobiotics.dashboard.interfaces import IParametersHandler
class McssParamsExperimentController(McssParamsController):
    implements(IExperimentHandler)
    
    def perform(self):
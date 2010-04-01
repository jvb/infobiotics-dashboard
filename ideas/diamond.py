from enthought.traits.api import HasTraits
from enthought.traits.ui.api import Handler 



class Params(HasTraits):
    pass

class Experiment(HasTraits):#Params
    pass

class McssParams(Params):
    pass

class McssExperiment(McssParams, Experiment):
    pass




class ParamsHandler(Handler):
    pass

class ExperimentHandler(ParamsHandler):
    pass

class McssExperimentHandler(ExperimentHandler):
    pass




class ExpermientProgressHandler(Handler):
    pass

class McssExperimentProgressHandler(ExpermientProgressHandler):
    pass

class McssExperimentDashboardProgressHandler(McssExperimentProgressHandler):
    pass
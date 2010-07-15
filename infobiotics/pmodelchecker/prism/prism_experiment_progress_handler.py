from infobiotics.common.api import ExperimentProgressHandler
from enthought.traits.api import property_depends_on

class PRISMExperimentProgressHandler(ExperimentProgressHandler):
    pass
#    @on_trait_change('model.generations, model.parameter_optimization_subtotal, model.parameter_optimization_total, model.current_generation')
#    def update_progress(self):
#        self.progress = int((((self.model.parameter_optimization_subtotal/self.model.parameter_optimization_total)*100) + (100 * self.model.current_generation) / (100 * self.generations)) * 100)
     
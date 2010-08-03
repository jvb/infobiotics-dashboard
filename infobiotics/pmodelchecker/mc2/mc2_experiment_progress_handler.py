from infobiotics.core.experiment_progress_handler import ExperimentProgressHandler
from enthought.traits.api import on_trait_change

class MC2ExperimentProgressHandler(ExperimentProgressHandler):

    @on_trait_change('model.max_simulation, model.simulation')
    def update_progress(self):
        self.progress = int((100 / self.max_simulation) * self.simulation) 

#    @on_trait_change('model.max_simulation, model.simulation')
#    def update_message(self):
#        return 'MC2ExperimentProgressHandler._get_status()'

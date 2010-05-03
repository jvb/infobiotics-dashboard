from infobiotics.common.api import ExperimentProgressHandler
from enthought.traits.api import property_depends_on

class MC2ExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('max_simulation, simulation')
    def _get_progress(self):
        return (100 / self.max_simulation) * self.simulation 

    def _get_status(self):
        return 'MC2ExperimentProgressHandler._get_status()'

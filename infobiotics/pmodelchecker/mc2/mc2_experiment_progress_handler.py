from infobiotics.common.api import ExperimentProgressHandler
from enthought.traits.api import property_depends_on

class MC2ExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass

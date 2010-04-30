from infobiotics.shared.api import (
    ExperimentProgressHandler, property_depends_on,
)

class MC2ExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass

from infobiotics.shared.api import \
    ExperimentHandler
from infobiotics.mcss.api import \
    McssParamsHandler, McssProgressHandler, mcss_experient_view

class McssExperimentHandler(ExperimentHandler, McssParamsHandler):

    def __progress_handler_default(self):
        return McssProgressHandler(self.model)

    traits_view = mcss_experient_view

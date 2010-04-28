from infobiotics.shared.api import ExperimentView, ExperimentHandler 
from infobiotics.mcss.api import (
    McssParamsHandler, McssProgressHandler, mcss_params_group,
) 

mcss_experient_view = ExperimentView(
    mcss_params_group,
)

class McssExperimentHandler(ExperimentHandler, McssParamsHandler):

    traits_view = mcss_experient_view

    def __progress_handler_default(self):
        return McssProgressHandler(model=self)


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    
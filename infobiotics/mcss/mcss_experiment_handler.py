from infobiotics.common.api import ExperimentHandler, ExperimentView
from mcss_params_handler import McssParamsHandler
from mcss_params_group import mcss_params_group
from mcss_progress_handler import McssProgressHandler
from enthought.traits.ui.api import VGroup 

#mcss_experient_view = ExperimentView(
#    mcss_params_group,
#    id='mcss_experient_view',
#)

class McssExperimentHandler(ExperimentHandler, McssParamsHandler):

    traits_view = ExperimentView(
        mcss_params_group,
        id='McssExperimentHandler',
    )

    def __progress_handler_default(self):
        return McssProgressHandler(model=self)


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    
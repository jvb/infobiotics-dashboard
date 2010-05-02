from infobiotics.mcss.api import McssParamsHandler, McssProgressHandler
from infobiotics.common.api import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def __progress_handler_default(self):
        return McssProgressHandler(model=self)


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    
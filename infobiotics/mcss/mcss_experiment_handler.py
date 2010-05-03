from infobiotics.mcss.api import McssParamsHandler, McssExperimentProgressHandler
from infobiotics.common.api import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def __progress_handler_default(self):
        return McssExperimentProgressHandler(model=self.model)


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    
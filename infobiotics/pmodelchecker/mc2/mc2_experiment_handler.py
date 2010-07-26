from infobiotics.pmodelchecker.mc2.api import MC2ParamsHandler, MC2ExperimentProgressHandler
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class MC2ExperimentHandler(MC2ParamsHandler, PModelCheckerExperimentHandler):

    def __progress_handler_default(self):
        return MC2ExperimentProgressHandler(model=self.model) 


if __name__ == '__main__':
    execfile('mc2_experiment.py')
    
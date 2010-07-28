from infobiotics.pmodelchecker.prism.api import PRISMParamsHandler, PRISMExperimentProgressHandler 
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class PRISMExperimentHandler(PRISMParamsHandler, PModelCheckerExperimentHandler):
    
    def __progress_handler_default(self):
        return PRISMExperimentProgressHandler(model=self.model)

    def perform(self, info):
        super(PModelCheckerExperimentHandler, self).perform(info)


if __name__ == '__main__':
    execfile('prism_experiment.py')
    
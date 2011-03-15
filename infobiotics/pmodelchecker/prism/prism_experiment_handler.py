from infobiotics.pmodelchecker.prism.api import PRISMParamsHandler 
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class PRISMExperimentHandler(PRISMParamsHandler, PModelCheckerExperimentHandler):
    pass



if __name__ == '__main__':
    from prism_experiment import PRISMExperiment
    experiment = PRISMExperiment()
    experiment.load('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_prism.params')
    experiment.configure()

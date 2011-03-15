from infobiotics.pmodelchecker.mc2.api import MC2ParamsHandler
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class MC2ExperimentHandler(MC2ParamsHandler, PModelCheckerExperimentHandler):
    pass



if __name__ == '__main__':
    from mc2_experiment import MC2Experiment
    experiment = MC2Experiment()
    experiment.load('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_mc2.params')
    experiment.configure()

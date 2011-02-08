from infobiotics.pmodelchecker.mc2.api import MC2ParamsHandler
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class MC2ExperimentHandler(MC2ParamsHandler, PModelCheckerExperimentHandler):
    pass



if __name__ == '__main__':
    execfile('mc2_experiment.py')
    

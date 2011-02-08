from infobiotics.mcss.api import McssParamsHandler
from infobiotics.core.experiment_handler import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def show_results(self):
        import os.path
        if os.path.exists(self.model.data_file_):
            from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
            w = SimulationResultsDialog(filename=self.model.data_file_)
            from infobiotics.commons.qt4 import centre_window
            centre_window(w)
            w.show()
        else:
            print "Results file '%s' does not exist, plotting aborted." % self.model.data_file_



if __name__ == '__main__':
    from mcss_experiment import McssExperiment
    experiment = McssExperiment()
    experiment.load('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/simulation.params')
    experiment.runs = 1000
    experiment.configure()    

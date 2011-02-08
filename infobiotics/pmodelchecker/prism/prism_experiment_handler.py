from infobiotics.pmodelchecker.prism.api import PRISMParamsHandler#, PRISMExperimentProgressHandler 
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class PRISMExperimentHandler(PRISMParamsHandler, PModelCheckerExperimentHandler):
    
    def perform(self, info): #TODO remove?
        super(PModelCheckerExperimentHandler, self).perform(info)

    def _finished(self, success):
        #TODO close progress dialog
        if success:
            print 'got here'
#            self.show_results()
#
#    def show_results(self):
#        import os.path
#        if os.path.exists(self.model.data_file_):
#            from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
#            w = SimulationResultsDialog(filename=self.model.data_file_)
#            from infobiotics.commons.qt4 import centre_window
#            centre_window(w)
#            w.show()
#        else:
#            print "Results file '%s' does not exist, plotting aborted." % self.model.data_file_



if __name__ == '__main__':
    execfile('prism_experiment.py')

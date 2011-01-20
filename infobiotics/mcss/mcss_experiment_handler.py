from infobiotics.mcss.api import McssParamsHandler, McssExperimentProgressHandler
from infobiotics.core.experiment_handler import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def __progress_handler_default(self):
        return McssExperimentProgressHandler(model=self.model)

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
        if info.object.finished_successfully:
            print 'succeeded', self
            self.show_results()
        else:
            print 'failed', self
        
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
    execfile('mcss_experiment.py')
    

from infobiotics.mcsscmaes.api import McssCmaesParamsHandler, McssCmaesExperimentProgressHandler
from infobiotics.core.experiment_handler import ExperimentHandler

class McssCmaesExperimentHandler(McssCmaesParamsHandler, ExperimentHandler):

    def __progress_handler_default(self):
        return McssCmaesExperimentProgressHandler(model=self.model)

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
        self.show_results()
        
    def show_results(self):
        import os.path
        if os.path.exists(self.model.data_file_):
            from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget, centre_window
            w = McssResultsWidget(filename=self.model.data_file_)
            from infobiotics.commons.qt4 import centre_window
            centre_window(w)
            w.show()
        else:
            print "Results file '%s' does not exist, plotting aborted." % self.model.data_file_


if __name__ == '__main__':
    execfile('mcsscmaes_experiment.py')
    

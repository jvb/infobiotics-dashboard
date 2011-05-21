from infobiotics.mcss.mcss_params_handler import McssParamsHandler
from infobiotics.core.experiment_handler import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

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
            #TODO show message box instead


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    

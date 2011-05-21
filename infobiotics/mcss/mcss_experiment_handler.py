#TODO move to mcss_experiment.py?

from infobiotics.mcss.mcss_params_handler import McssParamsHandler
from infobiotics.core.experiment_handler import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def show_results(self):
#        print 'McssExperimentHandler.show_results'
        import os.path
        print self.model.data_file_
        if os.path.exists(self.model.data_file_):
            from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget, centre_window
            w = McssResultsWidget(filename=self.model.data_file_)
            from infobiotics.commons.qt4 import centre_window
            centre_window(w)
#            print 'show'
            w.show()
#            print 'shown'
            
        else:
            print "Results file '%s' does not exist, plotting aborted." % self.model.data_file_


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    

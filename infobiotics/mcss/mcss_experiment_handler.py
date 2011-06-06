from infobiotics.mcss.mcss_params_handler import McssParamsHandler
from infobiotics.core.experiment_handler import ExperimentHandler
from enthought.pyface.api import error
from PyQt4.Qt import qApp 

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def show_results(self): # called by ExperimentHandler._finished
        import os.path
        if os.path.exists(self.model.data_file_):
            from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget, centre_window
            w = McssResultsWidget(filename=self.model.data_file_)
            from infobiotics.commons.qt4 import centre_window
            centre_window(w)
            w.show()
            w.raise_()
            qApp.processEvents()
        else:
            error(self.info.ui, "Results file '%s' does not exist, plotting aborted." % self.model.data_file_)

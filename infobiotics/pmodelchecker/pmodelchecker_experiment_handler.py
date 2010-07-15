from infobiotics.common.api import ExperimentHandler

class PModelCheckerExperimentHandler(ExperimentHandler):
    pass
#    def show_results(self):
#        import os.path
#        if os.path.exists(self.model.data_file_):
#            from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
#            w = SimulationResultsDialog(filename=self.model.data_file_)
#            from infobiotics.commons.qt4 import centre_window
#            centre_window(w)
#            w.show()
#        else:
#            print 'never been here before'
#            from enthought.traits.ui.message import auto_close_message
#            auto_close_message(self.child.before)
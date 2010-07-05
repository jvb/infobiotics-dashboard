from infobiotics.mcss.api import McssParamsHandler, McssExperimentProgressHandler
from infobiotics.common.api import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def __progress_handler_default(self):
        return McssExperimentProgressHandler(model=self.model)

    def object_finished_changed(self, info):
        self.show_results()
#        super(McssExperimentHandler, self).object_finished_changed(info) #TODO
        
    def show_results(self):
        import os.path
        if os.path.exists(self.model.data_file_):
            from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
            w = SimulationResultsDialog(filename=self.model.data_file_)
            from infobiotics.commons.qt4 import centre_window
            centre_window(w)
            w.show()
        else:
            from enthought.traits.ui.message import auto_close_message
            auto_close_message(self.child.before)

if __name__ == '__main__':
    execfile('mcss_experiment.py')
    
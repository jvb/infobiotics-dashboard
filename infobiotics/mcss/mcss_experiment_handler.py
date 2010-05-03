from infobiotics.mcss.api import McssParamsHandler, McssExperimentProgressHandler
from infobiotics.common.api import ExperimentHandler

class McssExperimentHandler(McssParamsHandler, ExperimentHandler):

    def __progress_handler_default(self):
        return McssExperimentProgressHandler(model=self.model)

    def object_finished_changed(self, info):
        self.show_results()
        self._on_close(info)
        
    def show_results(self):
        from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, centre_window
        w = SimulationResultsDialog(filename=self.model.data_file_)
        from commons.qt4 import centre_window
        centre_window(w)
        w.show()

if __name__ == '__main__':
    execfile('mcss_experiment.py')
    
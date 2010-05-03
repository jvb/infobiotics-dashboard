from infobiotics.api import McssExperiment
from enthought.traits.api import Instance
from infobiotics.dashboard.app import InfobioticsDashboardWorkbenchApplication
from infobiotics.mcss.api import McssExperimentHandler, McssExperimentProgressHandler

class McssDashboardExperiment(McssExperiment):
    
    application = Instance(InfobioticsDashboardWorkbenchApplication)
    
    def _handler_default(self):
        return McssExperimentDashboardHandler(model=self, application=self.application)

class McssExperimentDashboardHandler(McssExperimentHandler):#, ExperimentDashboardHandler):

    application = Instance(InfobioticsDashboardWorkbenchApplication)

    def __progress_handler_default(self):
        return McssExperimentDashboardProgressHandler(model=self.model)

#    def _show_progress(self):
#        # maybe raise experiments queue view here (moved to new class ExperimentDashboardHandler)
#        super(McssExperimentDashboardHandler, self)._show_progress()

    def object_finished_changed(self, info):
        print 'McssExperimentHandler.object_finished_changed(self, info)'
        self.show_results()
        
    def show_results(self):
        from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog
        from infobiotics.dashboard.plugins.simulator_results.editor import SimulatorResultsEditor
        self.application.workbench.edit(
            obj=SimulationResultsDialog(filename=self.model.data_file_),
            kind=SimulatorResultsEditor,
            use_existing=False,
        )

class McssExperimentDashboardProgressHandler(McssExperimentProgressHandler):#, CancelExperimentMixin):

    def object_finished_changed(self, info):
        self._on_close(info)

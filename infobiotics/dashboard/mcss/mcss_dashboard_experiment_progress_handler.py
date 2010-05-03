from infobiotics.mcss.api import McssExperimentProgressHandler

class McssDashboardExperimentProgressHandler(McssExperimentProgressHandler):#, CancelExperimentMixin):

    def object_finished_changed(self, info): #TODO move to DashboardExperimentProgressHandler?
        self._on_close(info)

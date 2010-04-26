class McssExperimentDashboardHandler(McssExperimentHandler):

    _progress_handler = McssExperimentDashboardProgressHandler

    def _show_progress(self):
        pass
        print '%s._show_progress: delegating to McssExperimentHandler' % self
        super(McssExperimentDashboardHandler, self)._show_progress()


class McssExperimentDashboardProgressHandler(McssExperimentProgressHandler, CancelExperimentMixin):
    pass

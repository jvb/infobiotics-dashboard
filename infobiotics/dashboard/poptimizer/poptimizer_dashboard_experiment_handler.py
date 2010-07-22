class POptimizerExperimentDashboardHandler(POptimizerExperimentHandler):

    _progress_handler = POptimizerExperimentDashboardProgressHandler

    def _show_progress(self):
        print 'POptimizerExperimentDashboardHandler._show_progress'

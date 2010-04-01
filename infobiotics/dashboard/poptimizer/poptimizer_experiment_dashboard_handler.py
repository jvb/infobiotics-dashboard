class POptimizerExperimentDashboardHandler(POptimizerExperimentHandler):

    _progress_handler = POptimizerExperimentDashboardProgressHandler

    def _show_progress(self):
        print 'got here'

from infobiotics.mcss.mcss_experiment_handler import McssExperimentHandler
from infobiotics.dashboard.core.dashboard_experiment_handler import DashboardExperimentHandler

class McssDashboardExperimentHandler(DashboardExperimentHandler, McssExperimentHandler):

	def show_results(self):
		''' Called by McssExperimentHandler.object_finished_changed '''
		from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget
		from infobiotics.dashboard.mcss.results.editor import McssResultsEditor
		obj = McssResultsWidget(filename=self.model.data_file_)
		if obj.loaded:
			self.application.workbench.edit(
				obj=obj,
				kind=McssResultsEditor,
				use_existing=False,
			)
		

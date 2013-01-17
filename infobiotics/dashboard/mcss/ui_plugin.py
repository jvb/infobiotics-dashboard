from traits.api import List, Instance, on_trait_change
from envisage.api import Plugin#, contributes_to
#from pyface.workbench.api import Perspective, PerspectiveItem
#from traits.etsconfig.api import ETSConfig
from pyface.workbench.api import IWorkbench
from pyface.api import GUI


from action_set import McssActionSet
from infobiotics.mcss.mcss_preferences import McssParamsPreferencesPage

#import os


class McssUIPlugin(Plugin):

	# 'IPlugin' interface
	id = 'infobiotics.dashboard.mcss.ui_plugin.McssUIPlugin' # The plugin's unique identifier
	name = 'mcss' # The plugin's name (suitable for displaying to the user)

	# Contributions to extension points made by this plugin

	action_sets = List(contributes_to='envisage.ui.workbench.action_sets')
	def _action_sets_default(self):
		return [McssActionSet]

#	perspectives = List(contributes_to='envisage.ui.workbench.perspectives')
#	def _perspectives_default(self):
#		return []

#	views = List(contributes_to='envisage.ui.workbench.views')
#	def _views_default(self):
#		return []

	preferences_pages = List(contributes_to='envisage.ui.workbench.preferences_pages')
	def _preferences_pages_default(self):
		return [McssParamsPreferencesPage]

#	openers = List(contributes_to='infobiotics.dashboard.plugins.unified_open_action.unified_open_action_plugin.openers') #TODO
#	def _openers_default(self):
#		from openers import openers
#		return openers
	
#	experiments = List(contributes_to='infobiotics.dashboard.plugins.experiments.ui_plugin.experiments') #TODO
#	def _experiments_default(self):
#		from mcss_experiment import McssExperiment
#		return McssExperiment()
	
#	# file:///home/jvb/src/ETS_3.4.0/AppTools/docs/html/preferences/PreferencesInEnvisage.html
#	
#	preferences = List(contributes_to='envisage.preferences')
#	def _preferences_default(self):
#		return ['file://%s' % os.path.join(ETSConfig.application_data, 'preferences.ini')]


#	workbench = Instance(IWorkbench)
#
#	def start(self):
#		self.workbench = self.application.workbench
#
#	def stop(self):
#		self.workbench = None
#
#	@on_trait_change('workbench:window_created')
#	def _new_workbench_window_created(self, event):
#		try:
#			GUI.invoke_after(500.0, self.edit_new_mcss_experiment, event.window) # do it in the UI thread, not too fast for workbench_window to have been created and hopefully slow enough (not tested on a slow computer), but not too slow for user #@UndefinedVariable  
#		except AttributeError:
#			pass # give up
#		
	# Called by InfobioticsDashboardWorkbenchApplication._new_workbench_window_created
	def edit_new_mcss_experiment(self, window):
		from infobiotics.dashboard.core.dashboard_experiment_editor import DashboardExperimentEditor
		from infobiotics.dashboard.mcss.mcss_dashboard_experiment import McssDashboardExperiment

		window.edit(
			obj=McssDashboardExperiment(application=self.application),
			kind=DashboardExperimentEditor,
			use_existing=False
		)
	
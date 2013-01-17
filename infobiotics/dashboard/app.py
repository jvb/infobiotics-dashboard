from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from envisage.ui.workbench.api import WorkbenchApplication
from pyface.api import GUI, AboutDialog#, ImageResource, SplashScreen
from traits.api import Instance, on_trait_change#, Event
import infobiotics.__version__

from infobiotics.dashboard.mcss.ui_plugin import McssUIPlugin

class InfobioticsDashboardWorkbenchApplication(WorkbenchApplication):
	""" The Infobiotics Dashboard (Envisage Workbench) application. """

	# implements IApplication and WorkbenchApplication interfaces
	id = 'dashboard' # The application's globally unique Id.
	name = 'Infobiotics Dashboard %s' % infobiotics.__version__ # The name of the application (also used on window title bars etc)
#	icon = ImageResource('icons/application.png') # The icon used on window title bars etc #TODO

	def _preferences_default(self):
		''' Touch preferences file to make sure it exists. '''
		from infobiotics.preferences import preferences
		filename = preferences.filename
		import os.path
		if not os.path.exists(filename): 
			open(filename, 'w').close() 
		return preferences
	
	def _about_dialog_default(self):
		return AboutDialog(
			parent=self.workbench.active_window.control,
#			image = ImageResource('logo/infobiotics_logo-1'), #TODO
#			image = ImageResource('logo/infobiotics_logo-2'),
#			image = None, # crashes
			additions=[
				self.name,
				'by',
				'Jonathan Blakes',
				'with',
				'Francisco J. Romero Campero,',
				'Jamie Twycross,',
				'Claudio Lima,',
				'Hongqing Cao,',
				'James Smaldon,',
				'Pawel Widera',
				'and',
				'Natalio Krasnogor'
			]
		)	
	
	def _splash_screen_default(self): #TODO
#		splash_screen = SplashScreen(
#			image			 = ImageResource('logo/infobiotics_logo-2'),
##			show_log_messages = True,
#		)
#		return splash_screen
		return None

#	def run(self):
##		print 'running' #TODO logger
#		super(InfobioticsDashboardWorkbenchApplication, self).run()

#	def _started_fired(self):
#		pass

#	@on_trait_change('workbench:window_created')
#	def _new_workbench_window_created(self, event):
#		try:
###			self.edit_default_experiment() # nothing happens because we are not in the UI thread
##			GUI.invoke_later(self.edit_default_experiment) # too fast for workbench_window to have been created
#			GUI.invoke_after(500.0, self.edit_default_experiment, event.window) # hopefully slow enough on fast computer but not too slow for user 
#		except AttributeError:
#			pass # give up
#		
	mcss_ui_plugin = Instance(McssUIPlugin)

	@on_trait_change('workbench:window_created')
	def _new_workbench_window_created(self, event):
		try:
			GUI.invoke_after(500.0, self.mcss_ui_plugin.edit_new_mcss_experiment, event.window) # do it in the UI thread, not too fast for workbench_window to have been created and hopefully slow enough (not tested on a slow computer), but not too slow for user #@UndefinedVariable  
		except AttributeError:
			pass # give up


if __name__ == '__main__':
	execfile('run.py')

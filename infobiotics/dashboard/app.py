from traits.etsconfig.api import ETSConfig
from traits.has_traits import on_trait_change
from pyface.gui import GUI
ETSConfig.toolkit = 'qt4'

from envisage.ui.workbench.api import WorkbenchApplication
from pyface.api import AboutDialog, ImageResource, SplashScreen
from traits.api import Event
import infobiotics.__version__

class InfobioticsDashboardWorkbenchApplication(WorkbenchApplication):
    """ The Infobiotics Dashboard (Envisage Workbench) application. """

    # implements IApplication and WorkbenchApplication interfaces
    id = 'dashboard' # The application's globally unique Id.
    name = 'Infobiotics Dashboard %s' % infobiotics.__version__ # The name of the application (also used on window title bars etc)
#    icon = ImageResource('icons/application.png') # The icon used on window title bars etc #TODO

    @on_trait_change('workbench.window_created')
    def _window_created(self, event):
        try:
#            GUI.invoke_later(self.open_mcss)
            GUI.invoke_after(500.0, self.open_mcss)
        except AttributeError:
            pass
        
    def open_mcss(self):
        # infobiotics.dashboard.mcss.actions.McssExperimentAction.perform
        from infobiotics.dashboard.core.dashboard_experiment_editor import DashboardExperimentEditor
        from infobiotics.dashboard.mcss.mcss_dashboard_experiment import McssDashboardExperiment
        self.workbench.edit(
            obj=McssDashboardExperiment(application=self),
            kind=DashboardExperimentEditor,
            use_existing=False
        )
    
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
#            image = ImageResource('logo/infobiotics_logo-1'), #TODO
#            image = ImageResource('logo/infobiotics_logo-2'),
#            image = None, # crashes
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
#        splash_screen = SplashScreen(
#            image             = ImageResource('logo/infobiotics_logo-2'),
##            show_log_messages = True,
#        )
#        return splash_screen
        return None

#    def run(self):
##        print 'running' #TODO logger
#        super(InfobioticsDashboardWorkbenchApplication, self).run()

#    def _started_fired(self):
#        print 'started' #TODO logger
    

if __name__ == '__main__':
    execfile('run.py')

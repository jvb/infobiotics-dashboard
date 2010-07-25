#from enthought.etsconfig.api import ETSConfig
#ETSConfig.toolkit = 'qt4'
#ETSConfig.company = 'infobiotics'

from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import AboutDialog, ImageResource, SplashScreen
from enthought.traits.api import Event

class InfobioticsDashboardWorkbenchApplication(WorkbenchApplication):
    """ The Infobiotics Dashboard (Envisage Workbench) application. """

    # implements IApplication and WorkbenchApplication interfaces
    id = 'dashboard' # The application's globally unique Id.
    name = 'Infobiotics Dashboard' # The name of the application (also used on window title bars etc)
#    icon = ImageResource('icons/application.png') # The icon used on window title bars etc #TODO
    
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
            parent = self.workbench.active_window.control,
#            image = ImageResource('logo/infobiotics_logo-1'), #TODO
#            image = ImageResource('logo/infobiotics_logo-2'),
            additions = [
                'Infobiotics Dashboard',
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

    def run(self):
#        print 'running' #TODO logger
        super(InfobioticsDashboardWorkbenchApplication, self).run()

#    def _started_fired(self):
#        print 'started' #TODO logger
    
    exiting = Event
    
    def exit(self):
        self.exiting = True # handlers listening for this event can act on it but not stop it
        super(InfobioticsDashboardWorkbenchApplication, self).exit()

if __name__ == '__main__':
    execfile('run.py')

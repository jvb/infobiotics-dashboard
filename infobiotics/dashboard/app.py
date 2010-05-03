from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import AboutDialog, ImageResource, SplashScreen

class InfobioticsDashboardWorkbenchApplication(WorkbenchApplication):
    """ The Infobiotics Dashboard (Envisage Workbench) application. """

    # implements IApplication and WorkbenchApplication interfaces
    id = 'infobiotics.dashboard.app' # The application's globally unique Id.
    name = 'Infobiotics Dashboard' # The name of the application (also used on window title bars etc)
#    icon = ImageResource('icons/application.png') # The icon used on window title bars etc
    
    def _about_dialog_default(self):
        return AboutDialog(
            parent = self.workbench.active_window.control,
#            image  = ImageResource('logo/infobiotics_logo-1'),
            image  = ImageResource('logo/infobiotics_logo-2'),
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
    
    def _splash_screen_default(self):
#        splash_screen = SplashScreen(
#            image             = ImageResource('logo/infobiotics_logo-2'),
##            show_log_messages = True,
#        )
#        return splash_screen
        return None

    def setup(self):
        ''' Call by infobiotics.dashboard.run.main() before 
        application.start()
        
        '''
        print 'setup' #TEST called automatically
#        print self.preferences.dump()
#        print self.preferences.get('dashboard.colour') # # green if flushed
#        print self.preferences.get('dashboard.colour', 'blue') # blue 
#        self.preferences.set('dashboard.colour', 'green')
#        print self.preferences.get('dashboard.colour') # green
#        self.preferences.flush() # write to file


if __name__ == '__main__':
    execfile('run.py')

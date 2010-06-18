# set TraitsUI backend 'toolkit' to 'qt4' and 'company' to 'Infobiotics' (used by ETSConfig.get_application_data())
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4' # set toolkit to 'qt4' (TraitsBackendQt) before any Traits imports; os.environ['ETS_TOOLKIT']='qt4' also works
ETSConfig.company = 'Infobiotics' # use ~/.infobiotics (or "Application Data\\Infobiotics") instead of ~/.enthought for preferences.ini

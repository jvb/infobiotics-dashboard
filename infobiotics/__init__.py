from __future__ import absolute_import

# allowing overriding of infobiotics package modules and subpackages 
try:
    __import__('pkg_resources').declare_namespace(__name__)
except:
    pass

# For py2app / py2exe support
try:
    import modulefinder
    for p in __path__:
        modulefinder.AddPackagePath(__name__, p)
except:
    pass

# setup version information
from infobiotics.__version__ import __version__, __version_info__
version = VERSION = __version__
version_info = VERSION_INFO = __version_info__ # __version_info__ is a tuple of int(major, minor, micro) 

# set PyQt4's QString API
import sip
#sip.setapi('QString', 2) # EPD > 3.6?
sip.setapi('QString', 1) # EPD <= 3.6? (Ubuntu Maverick and Natty use 3.4.1)

# set toolkit to 'qt4' (TraitsBackendQt) before any Traits imports; os.environ['ETS_TOOLKIT']='qt4' also works
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'#TODO PySide
# PySide signals and slots
#from PySide import QtCore
#QtCore.Signal = QtCore.pyqtSignal
#QtCore.Slot = QtCore.pyqtSlot

# set company to 'Infobiotics'
ETSConfig.company = 'Infobiotics'
# use ~/.infobiotics (or "Application Data\\Infobiotics" on Windows) instead of
# ~/.enthought for preferences.ini
# used by ETSConfig.get_application_data() for persistence (preferences)

#import preferences # fails on weasel

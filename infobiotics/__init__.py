from __future__ import absolute_import, with_statement, division

import os, sys

# set PyQt4 APIs compatible with EPD < 3.6
import sip
sip.setapi('QString', 1) 
sip.setapi('QVariant', 1)

from enthought.etsconfig.api import ETSConfig
ETSConfig.company = 'Infobiotics' # use ~/.infobiotics (or "Application Data\\Infobiotics" on Windows) instead of ~/.enthought for preferences.ini # used by ETSConfig.get_application_data() for persistence (preferences)
ETSConfig.toolkit = 'qt4' #os.environ['ETS_TOOLKIT']='qt4'

os.environ['QT_API'] = 'pyqt' # ETS >= 3.6

# fix matplotlib backend problems on Windows
if sys.platform.startswith('win'):
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE' # required for matplotlib with Numpy-MKL 1.6.1 MKL from http://www.lfd.uci.edu/~gohlke/pythonlibs/
    import matplotlib; matplotlib.use('qt4agg') # overrule configuration # http://www.py2exe.org/index.cgi/MatPlotLib
#    import pylab

#import preferences # fails on weasel #TODO

from .__version__ import __version__, __version_info__ 
version = VERSION = __version__
version_info = VERSION_INFO = __version_info__ # __version_info__ is a tuple of int(major, minor, micro) 

# set default log level for all loggers that use infobiotics.commons.api.logging (infobiotics.commons.unified_logging)  
from .commons.api import logging
logging.level = logging.ERROR

def tests(): '''Runs all tests.''' #TODO


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


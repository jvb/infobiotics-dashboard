# setup version information
from __version__ import __version__, __version_info__
version = VERSION = __version__
version_info = VERSION_INFO = __version_info__

# set TraitsUI backend 'toolkit' to 'qt4' and
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4' # set toolkit to 'qt4' (TraitsBackendQt) before any Traits imports; os.environ['ETS_TOOLKIT']='qt4' also works
#import sip
#sip.setapi('QString', 1)
#import enthought.pyface.ui.qt4.file_dialog

# set company to 'Infobiotics': 
# used by ETSConfig.get_application_data() for persistence (preferences)
ETSConfig.company = 'Infobiotics' # use ~/.infobiotics (or "Application Data\\Infobiotics") instead of ~/.enthought for preferences.ini


#------------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#------------------------------------------------------------------------------

from __future__ import absolute_import

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

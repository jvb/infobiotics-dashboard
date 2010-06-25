# find another way to import ProgressEditor, py2app's modulefinder fails with:
# ImportError 'enthought.pyface' if this is a package!

'''
This package adds missing modules to TraitsBackendQt
(http://pypi.python.org/pypi/TraitsBackendQt/).
'''
#------------------------------------------------------------------------------
# Copyright (c) 2007 by Enthought, Inc.
# All rights reserved.
#------------------------------------------------------------------------------

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
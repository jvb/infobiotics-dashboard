# Author: Prabhu Ramachandran
# License: BSD style
# Copyright (c) 2004, Enthought, Inc.
""" A Traits-based wrapper for the Visualization Toolkit.
Part of the Mayavi project of the Enthought Tool Suite.
"""

from os.path import exists, join, dirname, isdir, abspath

# The tvtk wrapper code is all typically inside one zip file.  We try to
# find this file and put it in __path__ and then create the 'tvtk' module
# wrapper from that.  If the ZIP file is extracted into a tvtk_classes
# directory the ZIP file is not used and the tvtk_classes directory is
# inserted into sys.path and the directory contents are used for the tvtk
# classes -- note that you must have the following structure
# tvtk_classes/tvtk_classes/__init__.py.  This is handy for tools like
# pydev (Eclipse).
##********************** NO LONGER TRUE *****************************
# We add the path to the local __path__ here, in the __init__, so that
# the unpickler can directly unpickle the TVTK classes.


#_zip = join(dirname(__file__), 'tvtk_classes.zip')
#tvtk_class_dir = join(dirname(__file__), 'tvtk_classes')
_zip = abspath(join('dist', 'tvtk', 'tvtk_classes.zip'))
tvtk_class_dir = abspath(join('dist', 'tvtk', 'tvtk_classes'))
#print dirname(__file__)
print
print __file__
print 'tvtk_class_dir', tvtk_class_dir
print '_zip', _zip
print

if exists(tvtk_class_dir) and isdir(tvtk_class_dir):
# Nothing to do, it will imported anyhow.
	print 'using tvtk_class_dir', tvtk_class_dir
elif exists(_zip):
	__path__.append(_zip)
	print 'using _zip', _zip
else:
	print 'error'
#	__path__.append(_zip)	
print '__path__', __path__

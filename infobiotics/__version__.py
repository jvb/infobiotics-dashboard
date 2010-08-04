'''
This file is automatically generated by setup.py, any changes must be made 
there or they will be lost.

__version__ is a str() of the form 'major.minor.micro' version number.

#__version_info__ is a tuple of (major, minor, micro, releaselevel, serial) 
#where releaselevel is in ('alpha', 'beta', 'candidate', 'final'). For example, 
#the "version_info value corresponding to the Python version 2.0 is 
#(2, 0, 0, 'final', 0)
__version_info__ is a tuple of int (major, minor, micro) 
'''

__version__ = '0.0.11'

__version_info__ = tuple([int(num) for num in __version__.split('.')[:3]]) # http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package/466694#466694


if __name__ == '__main__':
    print "__version__ = '" + __version__ + "'"
    print '__version_info__ =', __version_info__


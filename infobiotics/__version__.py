'''

__version__ is a str() of the form 'major.minor.micro' version number.

#__version_info__ is a tuple of (major, minor, micro, releaselevel, serial) 
#where releaselevel is in ('alpha', 'beta', 'candidate', 'final'). For example, 
#the "version_info value corresponding to the Python version 2.0 is 
#(2, 0, 0, 'final', 0) 
'''

import os.path

__version__ = open(os.path.join(os.path.split(__file__)[0], '../VERSION.txt')).read()

__version_info__ = tuple([int(num) for num in __version__.split('.')[:3]]) # http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package/466694#466694


if __name__ == '__main__':
    print __version__
    print __version_info__

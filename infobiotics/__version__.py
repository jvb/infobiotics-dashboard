'''
http://docs.python.org/library/sys.html
sys.version_info
A tuple containing the five components of the version number: major, minor, micro, releaselevel, and serial. All values except releaselevel are integers; the release level is 'alpha', 'beta', 'candidate', or 'final'. The version_info value corresponding to the Python version 2.0 is (2, 0, 0, 'final', 0). The components can also be accessed by name, so sys.version_info[0] is equivalent to sys.version_info.major and so on.
'''

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))
#TODO invert these adn write version from VERSION.txt

version = __version__
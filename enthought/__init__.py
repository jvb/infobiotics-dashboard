'''
This package adds missing modules to TraitsBackendQt
(http://pypi.python.org/pypi/TraitsBackendQt/).
'''

try:
    # if the code is ran from an egg, the namespace must be declared
    __import__('pkg_resources').declare_namespace(__name__)
except:
    pass

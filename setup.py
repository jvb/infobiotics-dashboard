'''
distutils install script for Infobiotics Dashboard

source distribution:
$ python setup.py sdist

Mac app:
$ python setup.py py2app

Windows executable:
$ python setup.py py2exe

'''

# bootstrap Distribute
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

# get correct pexpect for platform
import platform
if platform.system() == 'Windows':
    install_requires = [
#        'winpexpect>=1.3', # doesn't work
        'http://sage.math.washington.edu/home/goreckc/sage/wexpect/wexpect.py',
    ]
else:
    install_requires = [
        'pexpect>=2.4',
    ]

mainscript = 'bin/infobiotics-dashboard.py'

if platform.system() == 'Darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=dict(argv_emulation=True)),
    )
elif platform.system() == 'Windows':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
    )
else:
    extra_options = dict(
        scripts=[mainscript],
    )

setup(
    # PyPI metadata
    name='InfobioticsDashboard',
    author='Jonathan Blakes',
    author_email='jvb@cs.nott.ac.uk',
    license='COPYING.txt',#LICENSE.txt',
    url='http://www.infobiotics.org/infobiotics-workbench/',
    description='Infobiotics Dashboard is a graphical front-end to the Infobiotics Workbench, a suite of tools for modelling and designing multi-cellular biological systems.',
    long_description=open('README.txt').read(),
    version=open('VERSION.txt').read(),
    keywords='biology, modelling, simulation',
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',          
    ],

    packages=find_packages(
        exclude=[
            "*.tests", "*.tests.*", "tests.*", "tests", # http://packages.python.org/distribute/setuptools.html#using-find-packages
            'expect',
        ]
    ),

    install_requires = install_requires + [
        'EnthoughtBase>=3.0.4',
        'AppTools>=3.3.1',
        'Traits>=3.3.0',
        'EnvisageCore>=3.1.2',
        'TraitsGUI>=3.3.0',
        'EnvisagePlugins>=3.1.2',
        'TraitsBackendQt>=3.3.0',
        'Mayavi>=3.3.1',
        'configobj',#==4.7.2',
#        'tables>=2.1.2',
        'pytables>=2.1.2',
#        'which==1.1.0', # in infobiotics.thirdparty

#        'winpexpect==1.2', # done outside setup()
#        'pexpect==2.4', # done outside setup()

#        'numpy>=1.2.1', # can't be easy_installed
#        'Matplotlib==0.99.1', # can't be easy_installed either
    ],

    **extra_options # http://svn.pythonmac.org/py2app/py2app/trunk/doc/index.html#cross-platform
)

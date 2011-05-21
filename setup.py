'''
distutils install script for Infobiotics Dashboard

Install locally.
$ python setup.py install

Build source distribution:
$ python setup.py sdist

Build Mac app:
$ bash py2app.sh

Build Windows executable:
$ bash py2exe.sh

Build Debian package:
./make-deb.sh

'''

# bootstrap install Distribute
import setuptools #TODO bit suspicious about this but Jamie said it was OK.
from distribute_setup import use_setuptools
use_setuptools()

# packages that might get bundled by modulefinder by aren't ever used
EXCLUDES = [
    'Tkinter',
    'Tkconstants',
    'tcl',
    '_tkinter',
    'numpy.f2py',
    'wx',
    '_gtkagg',
    '_tkagg',
    'wxagg',
    'bsddb',
    'curses',
    'pywin.debugger',
    'pywin.debugger.dbgcon',
    'pywin.dialogs',
    'pydoc',
#    'doctest', 
    'test',
    'sqlite3'

    'mayavi.html',
]

import matplotlib
import glob
import sys
if sys.platform.startswith('darwin'):
    extra_options = dict(
        setup_requires=['py2app', 'pexpect'],
        app=['bin/infobiotics-dashboard.py'],
        options=dict(
            py2app=dict(
                argv_emulation=True, # cross-platform applications generally expect sys.argv to be used for opening files
                includes=['py2imports'], # better than INCLUDES?
                excludes=EXCLUDES,
                frameworks=[
#                    '/Library/Frameworks/Python.framework/Versions/6.1/lib/libfreetype.6.dylib', # done in py2app.sh as an arg to py2exe (which would override this...?)
#                    '/Library/Frameworks/Python.framework/Versions/Current/lib/libhdf5.6.dylib', # doesn't work from here, done in py2app.sh instead
                ],
                plist=dict(
                    # http://us.pycon.org/media/2010/talkdata/PyCon2010/038/paper.html#id18
#                    LSPrefersPPC=True,
                    CFBundleIdentifier='org.infobiotics.infobiotics-workbench',
                    CFBundleGetInfoString='The Infobiotics Dashboard, part of the Infobiotics Workbench.',
                    LSBackgroundOnly=False, # If True, the bundle will be a faceless background application.
                    LSUIElement=False, # If True, the bundle will be an agent application. It will not appear in the Dock or Force Quit window, but still can come to the foreground and present a UI.
#                    CFBundleURLTypes = [{}], # An array of dictionaries describing URL schemes supported by the bundle.
#                    NSServices = [{}] # An array of dictionaries specifying the services provided by the application.
                    CFBundleDocumentTypes=[ # http://us.pycon.org/media/2010/talkdata/PyCon2010/038/paper.html#associating-actions-with-file-types
#                        {
#                            'CFBundleTypeExtensions': ['html','htm'],
#                            'CFBundleTypeName': 'HTML Document',
#                            'CFBundleTypeRole': 'Viewer',
#                            'CFBundleTypeIconFile': 'Icon.icns',
#                        },
                        {
                            'CFBundleTypeExtensions' : ['h5'],
                            'CFBundleTypeName': 'mcss simulation',
                            'CFBundleTypeRole': 'Viewer',
                            'CFBundleTypeIconFile': 'mcss_simulation.icns',
                        },
                        {
                            'CFBundleTypeExtensions' : ['lpp', 'sps', 'plb', 'lat'],
                            'CFBundleTypeName': 'Lattice Population P System model file',
                            'CFBundleTypeRole': 'Viewer',
                            'CFBundleTypeIconFile': 'lattice_population_p_system_model_file.icns',
                        },
                    ],

                ),
            ),
        ),
        data_files=[
#            ("images", glob.glob("images/*.png")), #TODO
#            ("enthought/pyface/images", glob.glob("/Library/Frameworks/.framework/Versions/Current/lib/python26/site-packages/enthought/pyface/images/*.png")), #FIXME
        ] + matplotlib.get_py2exe_datafiles(), # http://www.py2exe.org/index.cgi/MatPlotLib
)
elif sys.platform.startswith('win'):

    # http://markmail.org/thread/qkdwu7gbwrmop6so
    try:
        import py2exe
        # ModuleFinder can't handle runtime changes to __path__, but win32com uses them
        import sys
        import pywintypes
        import pythoncom
        import win32api
        # if this doesn't work, try import modulefinder
        import py2exe.mf as modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]: #,"win32com.mapi"
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError, e:
        sys.stderr.write('%s\n' % e)

    import sys # needed for sys.prefix in mayavi_preferences and data_files below

    # touch mayavi preferences.ini #TODO should probably be in py2exe.sh but since this only happens if we call 'python setup.py py2exe' it is probably ok here.
    import os
    mayavi_preferences = os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\mayavi\\preferences\\preferences.ini')
    if not os.path.exists(mayavi_preferences):
        open(mayavi_preferences, 'w').close()

    # contents of manifest file that allow py2exe frozen apps to use the XP look and feel
    manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>Your Application</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

    extra_options = dict(
        setup_requires=['py2exe'],
        windows=[
            'bin/infobiotics-dashboard.pyw', #TODO see dict below
#            dict(
#                script="bin/infobiotics-dashboard.pyw", # .pyw are launched without opening a console window
##               "icon_resources": [(2, "images/example.ico")], #TODO If you have a windows icon, this is where to specify it
#                other_resources=[(24,1,manifest)],
#            ),
        ],
#        zipfile = None,
        options=dict(
            py2exe=dict(
                includes=['py2imports'],
                excludes=EXCLUDES,
                dll_excludes=[
                    "mswsock.dll", "powrprof.dll", "MSVCP90.dll", # http://stackoverflow.com/questions/1979486/py2exe-win32api-pyc-importerror-dll-load-failed
#                    'libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll', 'tk84.dll', # http://www.py2exe.org/index.cgi/MatPlotLib
                ],
                packages=["win32api", 'matplotlib', 'pytz'], # http://www.py2exe.org/index.cgi/MatPlotLib               
                unbuffered=True,
                optimize=0,
                bundle_files=3,
                skip_archive=True, # required so that it is easier to unzip tvtk_classes.zip
            )
        ),
        data_files=[
#            ("images", glob.glob("images/*.png")), #TODO
#            ("Microsoft.VC90.CRT",glob.glob("Microsoft.VC90.CRT/*")),
#            ("",glob.glob("Microsoft.VC90.CRT/*")), # removed from MANIFEST.in
            ("enthought/pyface/images", glob.glob(os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\pyface\\images\\*.png'))),
            ('enthought/mayavi/preferences', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\mayavi\\preferences\\preferences.ini')]),
            ('enthought/tvtk/plugins/scene', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\tvtk\\plugins\\scene\\preferences.ini')]),
            ('enthought/mayavi/core/lut', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\mayavi\\core\\lut\\pylab_luts.pkl')]),
            ('enthought/envisage/ui/workbench', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\envisage\\ui\\workbench\\preferences.ini')]),
        ] + matplotlib.get_py2exe_datafiles(), # http://www.py2exe.org/index.cgi/MatPlotLib
    )
else: # assume sys.platform.startswith('linux'):
    extra_options = dict(
        scripts=[
            'bin/infobiotics-dashboard',
            'bin/npz_info', #TODO add for Windows and Mac also
        ],
        data_files=[
#            ("images", glob.glob("images/*.png")), #TODO
            ('/usr/share/applications', ['infobiotics-dashboard.desktop']),
            ('/usr/share/pixmaps', ['images/infobiotics-workbench.xpm', 'images/infobiotics-workbench.png']),
        ],
    )

# dependencies when doing 'python setup.py install' 
INSTALL_REQUIRES = [
    'EnthoughtBase>=3.0.4',
    'AppTools>=3.3.1',
    'Traits>=3.3.0',
    'EnvisageCore>=3.1.2',
    'TraitsGUI>=3.3.0',
    'EnvisagePlugins>=3.1.2',
    'TraitsBackendQt>=3.3.0',
    'Mayavi', #TODO >=3.4.0',
    'configobj', # for enthought.preferences
    'numpy', #>=1.3.0', 
#    'matplotlib',#,==0.99.1', 
#    'which==1.1.0', # in infobiotics.thirdparty - is that the same as this? http://code.google.com/p/which/
    'xlwt',
    'libsbml',
    'progessbar',
    'quantities',
    'setproctitle',
]
INSTALL_REQUIRES += ['winpexpect>=1.3'] if sys.platform.startswith('win') else ['pexpect'] # winpexpect is preferred over wexpect on Windows
INSTALL_REQUIRES += ['pytables>=2.1.2'] if sys.platform.startswith('darwin') else ['tables>=2.1.2'] # tables is called 'pytables' on Mac (at least it is in EPD)

CLASSIFIERS = [ # http://pypi.python.org/pypi?%3Aaction=list_classifiers
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
]

# get version from VERSION.txt just like other Infobiotics Workbench components
VERSION = open('VERSION.txt').read().strip('\n')

# write infobiotics/__version__.py with VERSION hard-coded into it
__version__py = """'''
This file is automatically generated by setup.py, any changes must be made 
there or they will be lost.

__version__ is a str() of the form 'major.minor.micro' version number.

#__version_info__ is a tuple of (major, minor, micro, releaselevel, serial) 
#where releaselevel is in ('alpha', 'beta', 'candidate', 'final'). For example, 
#the "version_info value corresponding to the Python version 2.0 is 
#(2, 0, 0, 'final', 0)
__version_info__ is a tuple of int (major, minor, micro) 
'''

__version__ = '%s'

__version_info__ = tuple([int(num) for num in __version__.split('.')[:3]]) # http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package/466694#466694


if __name__ == '__main__':
    print "__version__ = '" + __version__ + "'"
    print '__version_info__ =', __version_info__

""" % VERSION
open('infobiotics/__version__.py', 'w').write(__version__py)

from setuptools import setup, find_packages
setup(
    # PyPI metadata
    version=VERSION,
    name='InfobioticsDashboard',
    author='Jonathan Blakes',
    author_email='jvb@cs.nott.ac.uk',
    license='COPYING.txt',
    url='http://www.infobiotics.org/infobiotics-workbench/',
    description='Infobiotics Dashboard is a graphical front-end to the Infobiotics Workbench, a suite of tools for modelling and designing multi-cellular biological systems.',
    long_description=open('README.txt').read(),
    keywords='biology, modelling, modeling, simulation',
    classifiers=CLASSIFIERS,
    platforms='any',

    packages=find_packages(
        exclude=[
#            '*.tests', '*.tests.*', 'tests.*', 'tests', # http://packages.python.org/distribute/setuptools.html#using-find-packages
#            'infobiotics.tests',
        ]
    ),

    install_requires=INSTALL_REQUIRES,
#    requires=[''],
#    provides=[
#        ('InfobioticsDashboard','') #TODO
#    ],
#    obseletes=[
#        ('InfobioticsDashboard','') #TODO
#    ],

    **extra_options
)

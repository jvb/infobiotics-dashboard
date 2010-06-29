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
from distribute_setup import use_setuptools
use_setuptools()


## Manifest file to allow py2exe to use the winxp look and feel
#manifest = """
#<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
#<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
#manifestVersion="1.0">
#<assemblyIdentity
#    version="0.64.1.0"
#    processorArchitecture="x86"
#    name="Controls"
#    type="win32"
#/>
#<description>Your Application</description>
#<dependency>
#    <dependentAssembly>
#        <assemblyIdentity
#            type="win32"
#            name="Microsoft.Windows.Common-Controls"
#            version="6.0.0.0"
#            processorArchitecture="X86"
#            publicKeyToken="6595b64144ccf1df"
#            language="*"
#        />
#    </dependentAssembly>
#</dependency>
#</assembly>
#"""

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
#                includes=INCLUDES,
                includes=['py2imports'], # better than INCLUDES?
                frameworks=[
#                    '/Library/Frameworks/Python.framework/Versions/6.1/lib/libfreetype.6.dylib',
                ],
#                plist=dict(
#                    # http://us.pycon.org/media/2010/talkdata/PyCon2010/038/paper.html#id18
##                    LSPrefersPPC=True,
#                    CFBundleIdentifier='org.infobiotics.infobiotics-workbench',
#                    CFBundleGetInfoString='The Infobiotics Dashboard, part of the Infobiotics Workbench.',
#                    LSBackgroundOnly=False, # If True, the bundle will be a faceless background application.
#                    LSUIElement=False, # If True, the bundle will be an agent application. It will not appear in the Dock or Force Quit window, but still can come to the foreground and present a UI.
##                    CFBundleURLTypes = [{}], # An array of dictionaries describing URL schemes supported by the bundle.
##                    NSServices = [{}] # An array of dictionaries specifying the services provided by the application.
#                    CFBundleDocumentTypes=[ # http://us.pycon.org/media/2010/talkdata/PyCon2010/038/paper.html#associating-actions-with-file-types
##                        {
##                            'CFBundleTypeExtensions': ['html','htm'],
##                            'CFBundleTypeName': 'HTML Document',
##                            'CFBundleTypeRole': 'Viewer',
##                            'CFBundleTypeIconFile': 'Icon.icns',
##                        },
#                        {
#                            'CFBundleTypeExtensions' : ['h5'], 
#                            'CFBundleTypeName': 'mcss simulation',
#                            'CFBundleTypeRole': 'Viewer',
#                            'CFBundleTypeIconFile': 'mcss_simulation.icns',
#                        },
#                        { 
#                            'CFBundleTypeExtensions' : ['lpp','sps','plb','lat'],
#                            'CFBundleTypeName': 'Lattice Population P System model file',
#                            'CFBundleTypeRole': 'Viewer',
#                            'CFBundleTypeIconFile': 'lattice_population_p_system_model_file.icns',
#                        },    
#                    ],
#                    
#                ),
            ),
        ), 
        data_files=[
#            ("images", glob.glob("images/*.png")), #TODO
#            ("enthought/pyface/images", glob.glob("/Library/Frameworks/.framework/Versions/Current/lib/python26/site-packages/enthought/pyface/images/*.png")), #FIXME
        ],
)
elif sys.platform.startswith('win'):
    try:
        import py2exe
       
        # http://markmail.org/thread/qkdwu7gbwrmop6so
        
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
        
    extra_options = dict(
        setup_requires=['py2exe'],
        windows=[
            'bin/infobiotics-dashboard.pyw', # .pyw are launched without opening a console window
#            dict(
#                script="bin/infobiotics-dashboard.pyw",
#                other_resources=[(24,1,manifest)],
#                # If you have a windows icon, this is where to specify it
##               "icon_resources": [(2, "images/example.ico")],
#            ),
        ],
        options=dict(
            py2exe=dict(
###                includes=['sip','PyQt4._qt'], # http://www.py2exe.org/index.cgi/Py2exeAndPyQt
##                includes=INCLUDES,# + ['pywintypes'], #'includes': ['py2exe_includes'], # http://markmail.org/thread/qkdwu7gbwrmop6so
#                includes=INCLUDES,
                includes=['py2imports'], # better than INCLUDES?
                excludes=[
                    'Tkinter', 
                    'Tkconstants', 
                    'tcl', 
                    '_tkinter', 
                    'numpy.f2py',
                    'wx',
                ],
                dll_excludes=["mswsock.dll", "powrprof.dll"], # http://stackoverflow.com/questions/1979486/py2exe-win32api-pyc-importerror-dll-load-failed
                packages=["win32api", 'matplotlib', 'pytz'], # http://www.py2exe.org/index.cgi/MatPlotLib               
                skip_archive=True, # required so that it is easier to unzip tvtk_classes.zip (?)
 #               bundle_files=2,
                unbuffered=True,
##                optimize=2,
#                optimize=0, # default (?) but best to be explicit
            )
        ),
        data_files=[        
#            ("images", glob.glob("images/*.png")), #TODO
            ("enthought/pyface/images", glob.glob("C:\/Python26/Lib/site-packages/enthought/pyface/images/*.png")), #TODO
            ('enthought/mayavi/preferences', ['C:\/Python26/Lib/site-packages/enthought/mayavi/preferences/preferences.ini']),
            ('enthought/tvtk/plugins/scene', ['C:\/Python26/Lib/site-packages/enthought/tvtk/plugins/scene/preferences.ini']),
            ('enthought/mayavi/core/lut', ['C:\/Python26/Lib/site-packages/enthought/mayavi/core/lut/pylab_luts.pkl']),
            ('enthought/envisage/ui/workbench', ['C:\/Python26/Lib/site-packages/enthought/envisage/ui/workbench/preferences.ini']),
        ] + matplotlib.get_py2exe_datafiles(), # http://www.py2exe.org/index.cgi/MatPlotLib
    )
else: # assume sys.platform.startswith('linux'):
    extra_options = dict(
        scripts=['bin/infobiotics-dashboard'],
        data_files=[
#        ("images", glob.glob("images/*.png")), #TODO
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
    'Mayavi',
    'configobj', # for enthought.preferences
    'numpy',#>=1.3.0', 
    'matplotlib'#,==0.99.1', 
#    'which==1.1.0', # in infobiotics.thirdparty
]
INSTALL_REQUIRES += ['winpexpect>=1.3'] if sys.platform.startswith('win') else ['pexpect'] # winpexpect is preferred over wexpect on Windows
INSTALL_REQUIRES += ['pytables>=2.1.2'] if sys.platform.startswith('darwin') else ['tables>=2.1.2'] # tables is called 'pytables' on Mac (at least it is in EPD)

CLASSIFIERS=[ # http://pypi.python.org/pypi?%3Aaction=list_classifiers
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

VERSION=open('VERSION.txt').read().strip('\n')

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


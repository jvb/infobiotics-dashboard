'''
distutils install script for Infobiotics Dashboard

Source distribution:
$ python setup.py sdist

Mac app:
$ python setup.py py2app

Windows executable:
$ python setup.py py2exe

Debian package:
./make-deb.sh

'''

# bootstrap install Distribute
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'EnthoughtBase>=3.0.4',
    'AppTools>=3.3.1',
    'Traits>=3.3.0',
    'EnvisageCore>=3.1.2',
    'TraitsGUI>=3.3.0',
    'EnvisagePlugins>=3.1.2',
    'TraitsBackendQt>=3.3.0',
    'Mayavi',
    'configobj',
#    'which==1.1.0', # in infobiotics.thirdparty
    'tables>=2.1.2',
    'numpy',#>=1.3.0', 
    'matplotlib'#,==0.99.1', 
]

# get correct pexpect for platform
import sys
if sys.platform.startswith('win'):
    INSTALL_REQUIRES += [
#        'winpexpect>=1.3', #TODO doesn't work! 
#        'wexpect==507', #TODO use 'http://sage.math.washington.edu/home/goreckc/sage/wexpect/wexpect.py' instead
    ]
else: # assume POSIX
    INSTALL_REQUIRES += [
        'pexpect',
    ]

# explicitly include hard-to-find modules for py2app #TODO and py2exe
INCLUDES = [
    'sip',
    'PyQt4',
    'PyQt4.Qsci',
    'PyQt4.QtNetwork',
    'enthought.traits.ui.qt4',
    'enthought.pyface.ui.qt4.action.action_item',
    'enthought.pyface.ui.qt4.action.menu_manager',
    'enthought.pyface.ui.qt4.action.menu_bar_manager',
    'enthought.pyface.ui.qt4.action.status_bar_manager',
    'enthought.pyface.ui.qt4.action.tool_bar_manager',
    'enthought.tvtk.vtk_module',
    'enthought.tvtk.pyface.ui.qt4.init',
    'enthought.tvtk.pyface.ui.qt4',
    'enthought.tvtk.pyface.ui.qt4.scene_editor',
    'enthought.pyface.ui.qt4.about_dialog',
    'enthought.pyface.ui.qt4.application_window',
    'enthought.pyface.ui.qt4.clipboard',
    'enthought.pyface.ui.qt4.confirmation_dialog',
    'enthought.pyface.ui.qt4.dialog',
    'enthought.pyface.ui.qt4.directory_dialog',
    'enthought.pyface.ui.qt4.file_dialog',
    'enthought.pyface.ui.qt4.gui',
    'enthought.pyface.ui.qt4.heading_text',
    'enthought.pyface.ui.qt4.image_cache',
    'enthought.pyface.ui.qt4.image_resource',
    'enthought.pyface.ui.qt4.init',
    'enthought.pyface.ui.qt4.message_dialog',
    'enthought.pyface.ui.qt4.progress_dialog',
    'enthought.pyface.ui.qt4.python_editor',
    'enthought.pyface.ui.qt4.python_shell',
    'enthought.pyface.ui.qt4.resource_manager',
    'enthought.pyface.ui.qt4.splash_screen',
    'enthought.pyface.ui.qt4.split_widget',
    'enthought.pyface.ui.qt4.system_metrics',
    'enthought.pyface.ui.qt4.widget',
    'enthought.pyface.ui.qt4.window',
    'enthought.pyface.ui.qt4.workbench.editor',
    'enthought.pyface.ui.qt4.workbench.split_tab_widget',
    'enthought.pyface.ui.qt4.workbench.view',
    'enthought.pyface.ui.qt4.workbench.workbench_window_layout',
    'enthought.envisage.ui.workbench.action.api',
    'enthought.plugins.ipython_shell.actions',
    'enthought.plugins.ipython_shell.actions.ipython_shell_actions',
    'enthought.plugins.refresh_code.actions',
    'enthought.plugins.remote_editor.actions',
    'enthought.plugins.text_editor.actions',
    'enthought.tvtk.plugins.scene.ui.actions',
    #TODO see py2exe_includes.py at http://markmail.org/thread/qkdwu7gbwrmop6so
    'numpy',
    'matplotlib',
    'vtk',
    'encodings',
    'tables',
]


# Manifest file to allow py2exe to use the winxp look and feel
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

import glob

if sys.platform.startswith('darwin'):
    extra_options = dict(
        setup_requires=['py2app'],
        app=['bin/infobiotics-dashboard.py'],
        options=dict(py2app=dict(argv_emulation=True, includes=INCLUDES)), # Cross-platform applications generally expect sys.argv to be used for opening files.
        data_files=[
#            ("images", glob.glob("images/*.png")), #TODO
#            ("enthought/pyface/images", glob.glob("/Library/Frameworks/.framework/Versions/Current/lib/python26/site-packages/enthought/pyface/images/*.png")), #FIXME
        ],
)
elif sys.platform.startswith('win'):
#    try:
#        import py2exe
#    except ImportError, e:
#        sys.stderr.write('%s\n' % e)
    extra_options = dict(
        setup_requires=['py2exe'],
        windows=['bin/infobiotics-dashboard.pyw'],
#        windows=[
#            dict(
#                script="bin/infobiotics-dashboard.pyw",
#                other_resources=[(24,1,manifest)],
#                # If you have a windows icon, this is where to specify it
##               "icon_resources": [(2, "images/example.ico")],
#            ),
#        ],
#        options={"py2exe" : {"includes" : ["sip", "PyQt4._qt"]}} # http://www.py2exe.org/index.cgi/Py2exeAndPyQt
        options=dict(
            py2exe=dict(
                includes=INCLUDES + ['pywintypes'], #'includes': ['py2exe_includes'], # http://markmail.org/thread/qkdwu7gbwrmop6so
                unbuffered=True,
                optimize=2,
                excludes=[
                    'Tkinter', 
                    'Tkconstants', 
                    'tcl', 
                    '_tkinter', 
                    'numpy.f2py',
                    'wx',
                ],
                dll_excludes=[ "mswsock.dll", "powrprof.dll" ], # http://stackoverflow.com/questions/1979486/py2exe-win32api-pyc-importerror-dll-load-failed
                packages=["win32api"],
                skip_archive=True,
                bundle_files=2,
            )
        ),
#        dependency_links=[
#            'http://sage.math.washington.edu/home/goreckc/sage/wexpect/wexpect.py#egg=wexpect-507',
#        ],
        data_files=[
#            ("images", glob.glob("images/*.png")), #TODO
            ("enthought/pyface/images", glob.glob("C:\/Python26/Lib/site-packages/enthought/pyface/images/*.png")), #TODO
            ('enthought/mayavi/preferences', ['C:\/Python26/Lib/site-packages/enthought/mayavi/preferences/preferences.ini']),
            ('enthought/tvtk/plugins/scene', ['C:\/Python26/Lib/site-packages/enthought/tvtk/plugins/scene/preferences.ini']),
            ('enthought/mayavi/core/lut', ['C:\/Python26/Lib/site-packages/enthought/mayavi/core/lut/pylab_luts.pkl']),
        ],
    )
else: # assume 'linux2'
    extra_options = dict(
        scripts=['bin/infobiotics-dashboard'],
        data_files=[
#        ("images", glob.glob("images/*.png")), #TODO
        ],
    )

VERSION=open('VERSION.txt').read().strip('\n')

setup(
    # PyPI metadata
    name='InfobioticsDashboard',
    author='Jonathan Blakes',
    author_email='jvb@cs.nott.ac.uk',
    license='COPYING.txt',
    url='http://www.infobiotics.org/infobiotics-workbench/',
    description='Infobiotics Dashboard is a graphical front-end to the Infobiotics Workbench, a suite of tools for modelling and designing multi-cellular biological systems.',
    long_description=open('README.txt').read(),
    keywords='biology, modelling, modeling, simulation',
    classifiers=[ # http://pypi.python.org/pypi?%3Aaction=list_classifiers
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
    platforms='any',

    packages=find_packages(
        exclude=[
            '*.tests', '*.tests.*', 'tests.*', 'tests', # http://packages.python.org/distribute/setuptools.html#using-find-packages
            'expect', #TODO
        ]
    ),

    install_requires=INSTALL_REQUIRES,
#    requires=[''],
    version=VERSION,
#    provides=[
#        ('InfobioticsDashboard','') #TODO
#    ],
#    obseletes=[
#        ('InfobioticsDashboard','') #TODO
#    ],
    
    **extra_options
)


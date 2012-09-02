'''
distutils install script for Infobiotics Dashboard

Install locally.
$ python setup.py install

Build source distribution:
$ python setup.py sdist

Build Mac app:
$ ./py2app.sh

Build Windows executable (under cygwin):
$ ./py2exe.sh

Build Linux executable:
$ ./bbfreeze.sh

Build Debian package:
./make-deb.sh

'''

# bootstrap install Distribute
#import setuptools #TODO bit suspicious about this but Jamie said it was OK.
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import glob
import sys
import os.path

# packages that might get bundled by modulefinder but are not needed
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
#	'doctest', 
	'test',
	'sqlite3'
	'mayavi.html',
]
''' more potential EXCLUDES: #TODO
AppKit
Carbon
Carbon.Files
DLFCN
ExtensionClass
Foundation
ICCProfile
IronPython.Runtime.Exceptions
IronPythonConsole
Numeric
PyObjCTools
System
System.Windows.Forms.Clipboard
_conditions_pro
_imaging_gif
_imagingagg
_scproxy
_transforms
_wxagg
builtins
cairo
cairo.gtk
clr
config
core.abs
core.max
core.min
core.round
dl
dnd_editor
fastnumpy
fastnumpy.mklfft
fltk
gobject
gtk
gtk.glade
hexdump
infobiotics.commons.traits.tests.test_relative_directory_and_params_relative_file.test_relative_directory_and_params_relative_file
infobiotics.dashboard.core.api
infobiotics.mcss.results.histograms2.EnhancedListWidget
infobiotics.mcss.results.histograms2.HistogramWidget
infobiotics.mcss.results.histograms2.SimulationDatasets
infobiotics.mcss.results.histograms2.SimulationWidgets
infobiotics.mcss.results.histograms2.Workbench
infobiotics.mcss.results.histograms2.actions
infobiotics.mcss.results.histograms2.functions
infobiotics.mcss.results.histograms2.md5sum
infobiotics.mcss.results.statistics
infobiotics.pmodelchecker.prism.api
ipy_completers
ipy_system_conf
jinja2.debugrenderer
lib.add_newdoc
libvtkCommonPython
libvtkFilteringPython
libvtkGenericFilteringPython
libvtkGeovisPython
libvtkGraphicsPython
libvtkHybridPython
libvtkIOPython
libvtkImagingPython
libvtkInfovisPython
libvtkParallelPython
libvtkRenderingPython
libvtkViewsPython
libvtkVolumeRenderingPython
libvtkWidgetsPython
matplotlib.backends._backend_gdk
matplotlib.backends._gtkagg
matplotlib.backends._macosx
mlab.amax
mlab.amin
modes.editingmodes
mpl_toolkits.natgrid
numarray
numarray.generic
numarray.records
numarray.strings
numpy.dft.old
numpy.lib.mlab
numpy.linalg.old
objc
ordered_set_editor
pango
pexpect
plot_editor
pretty
progressbar
projections.get_projection_class
projections.get_projection_names
projections.projection_factory
pydb
pydb.fns
pyemf
pygments.formatters.HtmlFormatter
pygments.formatters.LatexFormatter
pygments.formatters.TerminalFormatter
pygments.lexers.CLexer
pygments.lexers.PythonConsoleLexer
pygments.lexers.PythonLexer
pygments.lexers.RstLexer
pygments.lexers.TextLexer
pytz.zoneinfo
pywin.dialogs.list
qt
quantities
quantities.quantity
quantities.unitquantity
quantities.units
quantities.units.prefixes
quantities.units.substance
quantities.units.time
quantities.units.volume
resource
setproctitle
shell_editor
simplejson
site_mayavi
sitecustomize
startup
sysconfig
tables._parameters_pro
tables._table_pro
tables.index
tables.lrucacheExtension
testing.Tester
tvtk_classes
tvtk_classes.vtk_version
tvtk_local
ui_wizard
unittest.case
unittest.runner
user_mayavi
usercustomize
value_editor
wx.aui
wx.combo
wx.grid
wx.html
wx.lib.scrolledpanel
wx.py
wx.wizard
wxPython
numpy.Complex
numpy.Complex32
numpy.Complex64
numpy.Float
numpy.Float32
numpy.Float64
numpy.Int
numpy.Int16
numpy.Int32
numpy.Int8
numpy.UInt16
numpy.UInt32
numpy.UInt8
numpy.absolute
numpy.arccos
numpy.arccosh
numpy.arcsin
numpy.arcsinh
numpy.arctan
numpy.arctanh
numpy.bitwise_and
numpy.bitwise_or
numpy.bitwise_xor
numpy.bool_
numpy.ceil
numpy.complexfloating
numpy.conjugate
numpy.core.absolute
numpy.core.add
numpy.core.bitwise_and
numpy.core.bitwise_or
numpy.core.bitwise_xor
numpy.core.cdouble
numpy.core.complexfloating
numpy.core.conjugate
numpy.core.csingle
numpy.core.divide
numpy.core.double
numpy.core.equal
numpy.core.float64
numpy.core.float_
numpy.core.greater
numpy.core.greater_equal
numpy.core.inexact
numpy.core.intc
numpy.core.integer
numpy.core.invert
numpy.core.isfinite
numpy.core.isinf
numpy.core.isnan
numpy.core.left_shift
numpy.core.less
numpy.core.less_equal
numpy.core.ma
numpy.core.maximum
numpy.core.multiply
numpy.core.not_equal
numpy.core.number
numpy.core.power
numpy.core.remainder
numpy.core.right_shift
numpy.core.signbit
numpy.core.sin
numpy.core.single
numpy.core.sqrt
numpy.core.subtract
numpy.cosh
numpy.divide
numpy.fabs
numpy.floating
numpy.floor
numpy.floor_divide
numpy.fmod
numpy.greater
numpy.hypot
numpy.invert
numpy.isinf
numpy.left_shift
numpy.less
numpy.log
numpy.logical_and
numpy.logical_not
numpy.logical_or
numpy.logical_xor
numpy.maximum
numpy.minimum
numpy.negative
numpy.not_equal
numpy.power
numpy.random.rand
numpy.random.randn
numpy.remainder
numpy.right_shift
numpy.sign
numpy.sinh
numpy.tan
numpy.tanh
numpy.true_divide
numpy.uint
numpy.uint0
numpy.uint16
numpy.uint32
numpy.uint64
numpy.uintc
numpy.uintp
vtk.vtkVersion
'''

if sys.platform.startswith('darwin'):
	import matplotlib
	extra_options = dict(
		setup_requires=['py2app'], #, 'pexpect'], # done in INSTALL_REQUIRES
#		app=['bin/ibw.py'],#bin/infobiotics-dashboard.py'],
		app=['bin/infobiotics-dashboard.py'],
		options=dict(
			py2app=dict(
				argv_emulation=True, # cross-platform applications generally expect sys.argv to be used for opening files
				includes=['py2imports'], # better than INCLUDES?
				excludes=EXCLUDES,
#				frameworks=[
#					'/Library/Frameworks/Python.framework/Versions/6.1/lib/libfreetype.6.dylib', # done in py2app.sh as an arg to py2exe (which would override this...?)
#					'/Library/Frameworks/Python.framework/Versions/Current/lib/libhdf5.6.dylib', # doesn't work from here, done in py2app.sh instead
#				],
				plist=dict(
					# http://us.pycon.org/media/2010/talkdata/PyCon2010/038/paper.html#id18
#					LSPrefersPPC=True,
					CFBundleIdentifier='org.infobiotics.infobiotics-workbench',
					CFBundleGetInfoString='The Infobiotics Dashboard, part of the Infobiotics Workbench.',
					LSBackgroundOnly=False, # If True, the bundle will be a faceless background application.
					LSUIElement=False, # If True, the bundle will be an agent application. It will not appear in the Dock or Force Quit window, but still can come to the foreground and present a UI.
#					CFBundleURLTypes = [{}], # An array of dictionaries describing URL schemes supported by the bundle.
#					NSServices = [{}] # An array of dictionaries specifying the services provided by the application.
					CFBundleDocumentTypes=[ # http://us.pycon.org/media/2010/talkdata/PyCon2010/038/paper.html#associating-actions-with-file-types
#						{
#							'CFBundleTypeExtensions': ['html','htm'],
#							'CFBundleTypeName': 'HTML Document',
#							'CFBundleTypeRole': 'Viewer',
#							'CFBundleTypeIconFile': 'Icon.icns',
#						},
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
#			("images", glob.glob("images/*.png")), #TODO
#			("enthought/pyface/images", glob.glob("/Library/Frameworks/.framework/Versions/Current/lib/python26/site-packages/enthought/pyface/images/*.png")), #FIXME
		] + matplotlib.get_py2exe_datafiles(), # http://www.py2exe.org/index.cgi/MatPlotLib
	 )
elif sys.platform.startswith('win'):
	import matplotlib
	# http://markmail.org/thread/qkdwu7gbwrmop6so
	try:
		import py2exe
		# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
#		import sys
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

#	import sys # needed for sys.prefix in mayavi_preferences and data_files below

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
#			dict(
#				script="bin/infobiotics-dashboard.pyw", # .pyw are launched without opening a console window
##			   "icon_resources": [(2, "images/example.ico")], #TODO If you have a windows icon, this is where to specify it
#				other_resources=[(24,1,manifest)],
#			),
			'bin/infobiotics-workbench.pyw',
			'bin/ibw.pyw',
		],
		console=[
			'bin/ibw.py',
			'bin/infobiotics-dashboard.py',
			'bin/infobiotics-workbench.py',
		],
#		zipfile = None,
		options=dict(
			py2exe=dict(
				includes=['py2imports'],
				excludes=EXCLUDES,
				dll_excludes=[
					"mswsock.dll", "powrprof.dll", "MSVCP90.dll", # http://stackoverflow.com/questions/1979486/py2exe-win32api-pyc-importerror-dll-load-failed
#					'libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll', 'tk84.dll', # http://www.py2exe.org/index.cgi/MatPlotLib
				],
				packages=["win32api", 'matplotlib', 'pytz'], # http://www.py2exe.org/index.cgi/MatPlotLib			   
				unbuffered=True,
				optimize=0,
				bundle_files=3,
				skip_archive=True, # required so that it is easier to unzip tvtk_classes.zip
			)
		),
		data_files=[
#			("images", glob.glob("images/*.png")), #TODO
##			("Microsoft.VC90.CRT",glob.glob("Microsoft.VC90.CRT/*")),
#			("Microsoft.VC90.CRT",glob.glob("py2exe/Microsoft.VC90.CRT/*")),
##			("",glob.glob("Microsoft.VC90.CRT/*")), # removed from MANIFEST.in
#			("",glob.glob("py2exe/Microsoft.VC90.CRT/*")), # removed from MANIFEST.in
			("enthought/pyface/images", glob.glob(os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\pyface\\images\\*.png'))),
			('enthought/mayavi/preferences', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\mayavi\\preferences\\preferences.ini')]),
			('enthought/tvtk/plugins/scene', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\tvtk\\plugins\\scene\\preferences.ini')]),
			('enthought/mayavi/core/lut', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\mayavi\\core\\lut\\pylab_luts.pkl')]),
			('enthought/envisage/ui/workbench', [os.path.join(sys.prefix, 'Lib\\site-packages\\enthought\\envisage\\ui\\workbench\\preferences.ini')]),
		] + matplotlib.get_py2exe_datafiles(), # http://www.py2exe.org/index.cgi/MatPlotLib
	)
else:
	assert sys.platform.startswith('linux')
	extra_options = dict(
		scripts=[
			'bin/ibw',
			'bin/infobiotics-workbench',
			'bin/infobiotics-dashboard',
		],
		data_files=[
			('/usr/share/tvtk/tvtk_classes.zip', [os.path.join(sys.prefix, 'tvtk')]), #TODO
#			("images", glob.glob("images/*.png")), #TODO
			('/usr/share/applications', ['infobiotics-dashboard.desktop']),
			('/usr/share/pixmaps', ['images/infobiotics-workbench.xpm', 'images/infobiotics-workbench.png']),
		],
	)

# dependencies when doing 'python setup.py install' 
INSTALL_REQUIRES = [
##	'distribute', # http://pypi.python.org/pypi/distribute#quick-help-for-developers
#	'numpy>=1.4.0',
	'numpy',
	
	'apptools',
	'traits',
	'traitsui',
	'pyface',
	'envisage',
	
#	'EnthoughtBase>=3.0.4',
#	'AppTools>=3.3.2',
#	'Traits>=3.4.0',
#	'TraitsGUI>=3.4.0',
#	'EnvisageCore>=3.1.2',
#	'EnvisagePlugins>=3.1.2',
#	'TraitsBackendQt>=3.4.0',
	'Mayavi', #>=3.4.0',
	'configobj', # for apptools.preferences
	'matplotlib', #,==0.99.1', 
	'progressbar',
##	'which==1.1.0', # in infobiotics.thirdparty as there is no python-which package in Debian (also available from http://code.google.com/p/which/)
	'setproctitle',
	'xlwt',
#	'quantities',
##	'libsbml', #TODO
]
#INSTALL_REQUIRES += ['winpexpect>=1.3'] if sys.platform.startswith('win') else ['pexpect'] # winpexpect is preferred over wexpect on Windows
if not sys.platform.startswith('win'):
	INSTALL_REQUIRES += ['pexpect'] 
INSTALL_REQUIRES += ['pytables>=2.1.2'] if sys.platform.startswith('darwin') else ['tables>=2.1.2'] # tables is called 'pytables' on Mac (at least it is in EPD)


# get version from VERSION.txt just like other Infobiotics Workbench components
VERSION = open('VERSION.txt').read().strip()#'\n'
# write infobiotics/__version__.py with VERSION hard-coded into it
__version__py = """'''This file is automatically generated by setup.py, any changes must be made 
there or they will be lost.

__version__ is a str() of the form 'major.minor.micro' version number.

__version_info__ is a tuple of int (major, minor, micro)
'''

__version__ = '%s'

__version_info__ = tuple([int(num) for num in __version__.split('.')[:3]]) # http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package/466694#466694

#__version_info__ could be a tuple of (major, minor, micro, releaselevel, serial) 
#where releaselevel is in ('alpha', 'beta', 'candidate', 'final'). For example, 
#the "version_info value corresponding to the Python version 2.0 is 
#(2, 0, 0, 'final', 0)


if __name__ == '__main__':
	print "__version__ = '" + __version__ + "'"
	print '__version_info__ =', __version_info__

""" % VERSION
open('infobiotics/__version__.py', 'w').write(__version__py)


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
			'infobiotics.language',
		]
	),

	install_requires=INSTALL_REQUIRES,
#	requires=[''],

	**extra_options
)

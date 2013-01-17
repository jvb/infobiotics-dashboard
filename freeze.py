import os


#from bbfreeze.modulegraph import modulegraph
#modulegraph.AddPackagePath('tvtk.tvtk_classes', '/usr/share/pyshared/tvtk')
##modulegraph.ReplacePackage('tvtk.tvtk_classes', '/usr/share/pyshared/tvtk')


#def isRealModule(m):
#	from modulegraph.modulegraph import BadModule, MissingModule, ExcludedModule
#	print m
#	print 'isinstance(BadModule)', isinstance(m, BadModule)
#	print 'isinstance(MissingModule)', isinstance(m, MissingModule)
#	print 'isinstance(ExcludedModule)', isinstance(m, ExcludedModule)
#	if m is None or isinstance(m, (BadModule, MissingModule, ExcludedModule)):
#		return False
#	else:
#		return True
#recipes.isRealModule = isRealModule


from bbfreeze.recipes import isRealModule
from bbfreeze import recipes

# patch matplotlib recipe
def recipe_matplotlib(mf):
	m = mf.findNode('matplotlib')
	if not isRealModule(m):
		return
	import matplotlib
	if 0:  # do not copy matplotlibdata. assume matplotlib is installed as egg
		dp = matplotlib.get_data_path()
		assert dp
		mf.copyTree(dp, "matplotlibdata", m)
#	mf.import_hook("matplotlib.numerix.random_array", m)
	backend_name = 'backend_' + matplotlib.get_backend().lower()
	print "recipe_matplotlib: using the %s matplotlib backend" % (backend_name, )
	mf.import_hook('matplotlib.backends.' + backend_name, m)
	return True
recipes.recipe_matplotlib = recipe_matplotlib


#def include_whole_package(name, skip=lambda x: False):
#	def recipe(mf):
#		m = mf.findNode(name)
#		if not isRealModule(m):
#			return None
#
#		from bbfreeze.freezer import ZipModule
#		if isinstance(m, ZipModule):
#			return None
#
#		top = os.path.dirname(m.filename)
#		prefixlen = len(os.path.dirname(top)) + 1
#		for root, dirs, files in os.walk(top):
#			pkgname = root[prefixlen:].replace(os.path.sep, ".")
#			for f in files:
#				if not f.endswith(".py"):
#					continue
#
#				if f == "__init__.py":
#					modname = pkgname
#				else:
#					modname = "%s.%s" % (pkgname, f[:-3])
#
#				if not skip(modname):
#					mf.import_hook(modname, m, ['*'])
#		return True
#
#	recipe.__name__ = "recipe_" + name
#	return recipe
#recipes.include_whole_package = include_whole_package


# add tvtk_classes.zip recipe
###recipes.recipe_tvtk_classes = recipes.include_whole_package('tvtk.tvtk_classes')
##recipes.recipe_tvtk_classes = recipes.find_all_packages('tvtk')
#def recipe_tvtk_classes(mf):
#	m = mf.findNode('tvtk.api')
#	if not isRealModule(m):
#		exit("'not isRealModule(mf.findNode('tvtk.api')")
#		return
#
##	import tvtk
##	mf.copyTree(dp, "tvtk", m)
#	dp = '/usr/lib/python2.7/dist-packages/tvtk/'
##	mf.copyTree("test/", 'test', m)
##	mf.copyTree(dp, "library.zip/tvtk/", m)
#
##	mf.import_hook("tvtk.tvtk_classes", m)
#	
#	print "recipe_tvtk_classes"
#	return True
#recipes.recipe_tvtk_classes = recipe_tvtk_classes


#from bbfreeze import codehack
#
#def recipe_mayavi(mf):
###	m = mf.findNode('mayavi')
##	if not isRealModule(m):
##		return
##	print "recipe_mayavi begin"
##	mf.import_hook("mayavi.preferences", m)
##	t = os.path.join(os.path.dirname(m.filename), 'preferences')
###	print t
##	mf.copyTree(t, 'mayavi/preferences', m)
##	
##	print "recipe_mayavi end"
##	return True
#
#	m = mf.findNode('mayavi.preferences.preference_manager')
#	if not isRealModule(m):
#		return
#	print "recipe_mayavi begin"
#
#	import mayavi.preferences.preference_manager#.PreferenceManager
##	cls = mayavi.preferences.preference_manager.PreferenceManager
##	method = cls._load_preferences
##	m = mayavi.preferences.preference_manager.PreferenceManager
#	
#	repl = '''
#def _load_preferences(self):
#    """Load the default preferences."""
#    # debugging freezing with bbfreeze.sh (start)
#    print 'debugging freezing with bbfreeze.sh (start)'    
#
#    import sys
#    print 'sys.executable', sys.executable
#    print 'sys.path', sys.path
#
##       from traits.etsconfig.api import ETSConfig
##       ID = 'mayavi_e3'
##       print 'ID', ID
#    # Save current application_home.
#    app_home = ETSConfig.get_application_home()
#    print 'app_home', app_home
#    # Set it to where the mayavi preferences are temporarily.
#    path = join(ETSConfig.get_application_data(), ID)
#
##       if getattr(sys, "frozen", False):
##           path = join(sys.path[1], ID)
#
#    print 'path', path
#    ETSConfig.application_home = path
#    try:
#        for pkg in ('mayavi.preferences',
#                    'tvtk.plugins.scene'):
#            pref = 'preferences.ini'
#
#            print 'pkg', pkg
#            print 'pref', pref
#            print join(sys.path[1], pkg.replace('.', '/'), pref)
#            if getattr(sys, "frozen", False):
##                    pref_file = pkg_resources.resource_stream(join(sys.path[1], pkg.replace('.', '/'), pref))
#                pref_file = open(join(sys.path[1], pkg.replace('.', '/'), pref), 'rb')
#            else:
#                pref_file = pkg_resources.resource_stream(pkg, pref)
#
#        preferences = self.preferences
#        default = preferences.node('default/')
#        default.load(pref_file)
#        pref_file.close()
#    finally:
#        # Set back the application home.
#        ETSConfig.application_home = app_home
#'''
#	
#	m.code = codehack.replace_functions(m.code, repl)
#	
#	print "recipe_mayavi end"
#	return True
#recipes.recipe_mayavi = recipe_mayavi


from bbfreeze import Freezer 

Freezer.use_compression = False

f = Freezer(
	'dist',#'infobiotics-dasboard-1.1.0', 
	includes=(
#		'tvtk.tvtk_access',
	)
)
f.addScript('infobiotics-dashboard.py')
#f.addScript('bbfreeze_test.py')
f() # freeze


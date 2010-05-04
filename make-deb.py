#!/usr/bin/env python

from py2deb import Py2deb
p=Py2deb('infobiotics-dashboard')

p.author='Jonathan Blakes'
p.mail='jvb@cs.nott.ac.uk'
p.description='''Infobiotics Dashboard\

Infobiotics Dashboard is a graphical front-end to the Infobiotics Workbench,
a suite of tools for modelling and designing multi-cellular biological systems.
'''
p.url='http://www.infobiotics.org/infobiotics-workbench/' #TODO /dashboard/

p.depends='python-qt4, python-qscintilla2, '\
'python-numpy, '\
'python-tables, '\
'python-matplotlib, python-tk, '\
'python-traits, python-traitsgui, python-traitsbackendqt, '\
#'python-chaco, '\
'python-envisagecore, python-envisageplugins, '\
'python-apptools, '\
'mayavi2, '\
'libhdf5-serial-1.8.3, '\
'mcss, pmodelchecker, poptimizer'

p.license='gpl'
p.section='science'

#import os
#os.chdir('..')

p['/usr/share/doc/infobiotics-dashboard']=[
    'AUTHORS.txt',
    'COPYING.txt',
    'LICENSE.txt',
    'README.txt',
    'THANKS.txt',
    'VERSION.txt',
]

#find infobiotics -type f | egrep -v '(\/\.svn\/)|(\.pyc)'#|(\.ui)'

p['/usr/bin']=[
    'bin/infobiotics-dashboard|infobiotics-dashboard',
]

p['/usr/share/infobiotics-dashboard']=[
    'infobiotics/shared/__init__.py',
    'infobiotics/shared/colours.py',
    'infobiotics/shared/lists.py',
    'infobiotics/shared/md5sum.py',
    'infobiotics/shared/file_wrapper.py',
    'infobiotics/shared/traits_imports.py',
    'infobiotics/shared/extended_traits.py',
    'infobiotics/__init__.py',
    'infobiotics/dashboard/shared/__init__.py',
    'infobiotics/dashboard/shared/traits.py',
    'infobiotics/dashboard/shared/files.py',
    'infobiotics/dashboard/shared/mayavi.py',
    'infobiotics/dashboard/shared/unified_logging/__init__.py',
    'infobiotics/dashboard/shared/unified_logging/unified_logging.py',
    'infobiotics/dashboard/shared/unified_logging/uses_unified_logging.py',
    'infobiotics/dashboard/__init__.py',
    'infobiotics/dashboard/run.py',
    'infobiotics/dashboard/app.py',
    'infobiotics/dashboard/plugins/simulator_results/editor.py',
    'infobiotics/dashboard/plugins/simulator_results/__init__.py',
    'infobiotics/dashboard/plugins/simulator_results/simulator_results.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_plugin.py',
    'infobiotics/dashboard/plugins/simulator_results/actions.py',
    'infobiotics/dashboard/plugins/simulator_results/icons_rc.py',
    'infobiotics/dashboard/plugins/simulator_results/FromToDoubleSpinBox.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_plots_preview_dialog.py',
    'infobiotics/dashboard/plugins/simulator_results/PlotsListWidget.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_simulation_results_dialog.py',
    'infobiotics/dashboard/plugins/simulator_results/icons.qrc',
    'infobiotics/dashboard/plugins/simulator_results/action_set.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_player_control_widget.py',
    'infobiotics/dashboard/plugins/__init__.py',
    'infobiotics/dashboard/plugins/pmodelchecker/__init__.py',
    'infobiotics/dashboard/plugins/pmodelchecker/pmodelchecker_experiment_handler.py',
    'infobiotics/dashboard/plugins/pmodelchecker/mc2_experiment.py',
    'infobiotics/dashboard/plugins/pmodelchecker/results.psm',
    'infobiotics/dashboard/plugins/pmodelchecker/ui_plugin.py',
    'infobiotics/dashboard/plugins/pmodelchecker/pmodelchecker_experiment.py',
    'infobiotics/dashboard/plugins/pmodelchecker/actions.py',
    'infobiotics/dashboard/plugins/pmodelchecker/prism_group.py',
    'infobiotics/dashboard/plugins/pmodelchecker/TraitedPrismResults.py',
    'infobiotics/dashboard/plugins/pmodelchecker/mc2_group.py',
    'infobiotics/dashboard/plugins/pmodelchecker/temporal_formulas.py',
    'infobiotics/dashboard/plugins/pmodelchecker/pmodelchecker_action_set.py',
    'infobiotics/dashboard/plugins/pmodelchecker/prism_experiment.py',
    'infobiotics/dashboard/plugins/pmodelchecker/preferences_page.py',
    'infobiotics/dashboard/plugins/mcss/mcss_experiment.py',
    'infobiotics/dashboard/plugins/mcss/__init__.py',
    'infobiotics/dashboard/plugins/mcss/ui_plugin.py',
    'infobiotics/dashboard/plugins/mcss/actions.py',
    'infobiotics/dashboard/plugins/mcss/mcss_group.py',
    'infobiotics/dashboard/plugins/mcss/mcss_experiment_handler.py',
    'infobiotics/dashboard/plugins/mcss/action_set.py',
    'infobiotics/dashboard/plugins/mcss/preferences_page.py',
    'infobiotics/dashboard/plugins/workspace/__init__.py',
    'infobiotics/dashboard/plugins/workspace/views.py',
    'infobiotics/dashboard/plugins/workspace/ui_plugin.py',
    'infobiotics/dashboard/plugins/workspace/actions.py',
    'infobiotics/dashboard/plugins/workspace/tmp/file_test.py',
    'infobiotics/dashboard/plugins/workspace/plugin.py',
    'infobiotics/dashboard/plugins/workspace/perspectives.py',
    'infobiotics/dashboard/plugins/workspace/action_set.py',
    'infobiotics/dashboard/plugins/workspace/preferences_page.py',
    'infobiotics/dashboard/plugins/experiments/experiment_progress_item.py',
    'infobiotics/dashboard/plugins/experiments/params_experiment.py',
    'infobiotics/dashboard/plugins/experiments/experiment_queue.py',
    'infobiotics/dashboard/plugins/experiments/experiment.py',
    'infobiotics/dashboard/plugins/experiments/__init__.py',
    'infobiotics/dashboard/plugins/experiments/i_experiment_handler.py',
    'infobiotics/dashboard/plugins/experiments/progress_meter.py',
    'infobiotics/dashboard/plugins/experiments/progress_item.py',
    'infobiotics/dashboard/plugins/experiments/ui_plugin.py',
    'infobiotics/dashboard/plugins/experiments/actions.py',
    'infobiotics/dashboard/plugins/experiments/i_params_experiment.py',
    'infobiotics/dashboard/plugins/experiments/params_experiment_editor.py',
    'infobiotics/dashboard/plugins/experiments/experiment_handler.py',
    'infobiotics/dashboard/plugins/experiments/i_experiment.py',
    'infobiotics/dashboard/plugins/experiments/progress_dialog.py',
    'infobiotics/dashboard/plugins/experiments/params_experiment_handler.py',
    'infobiotics/dashboard/plugins/experiments/noninteractive_progress_meter.py',
    'infobiotics/dashboard/plugins/experiments/i_progress_meter.py',
    'infobiotics/dashboard/plugins/experiments/params_xml_reader.py',
    'infobiotics/dashboard/plugins/bnf/text_editor_handler.py',
    'infobiotics/dashboard/plugins/bnf/__init__.py',
    'infobiotics/dashboard/plugins/bnf/openers.py',
    'infobiotics/dashboard/plugins/bnf/views.py',
    'infobiotics/dashboard/plugins/bnf/lat_editor.py',
    'infobiotics/dashboard/plugins/bnf/ui_plugin.py',
    'infobiotics/dashboard/plugins/bnf/lpp_editor.py',
    'infobiotics/dashboard/plugins/bnf/actions.py',
    'infobiotics/dashboard/plugins/bnf/bnf_editor.py',
    'infobiotics/dashboard/plugins/bnf/bnf_file_trees.py',
    'infobiotics/dashboard/plugins/bnf/text_editor.py',
    'infobiotics/dashboard/plugins/bnf/sps_editor.py',
    'infobiotics/dashboard/plugins/bnf/bnf_action_set.py',
    'infobiotics/dashboard/plugins/bnf/plb_editor.py',
    'infobiotics/dashboard/plugins/example/__init__.py',
    'infobiotics/dashboard/plugins/example/views.py',
    'infobiotics/dashboard/plugins/example/ui_plugin.py',
    'infobiotics/dashboard/plugins/example/actions.py',
    'infobiotics/dashboard/plugins/example/plugin.py',
    'infobiotics/dashboard/plugins/example/perspectives.py',
    'infobiotics/dashboard/plugins/example/action_set.py',
    'infobiotics/dashboard/plugins/example/preferences_page.py',
    'infobiotics/dashboard/plugins/poptimizer/__init__.py',
    'infobiotics/dashboard/plugins/poptimizer/ui_plugin.py',
    'infobiotics/dashboard/plugins/poptimizer/actions.py',
    'infobiotics/dashboard/plugins/poptimizer/poptimizer_experiment.py',
    'infobiotics/dashboard/plugins/poptimizer/poptimizer_group.py',
    'infobiotics/dashboard/plugins/poptimizer/action_set.py',
    'infobiotics/dashboard/images/logo/infobiotics_logo-1.png',
    'infobiotics/dashboard/images/logo/infobiotics_logo-2.png',
    'infobiotics/dashboard/images/infobiotics_logo-1.png',
    'infobiotics/dashboard/images/infobiotics_logo-2.png',
]

p.arch='all'
version=open('VERSION','r').read()
changelog=open('ChangeLog','r').read()
p.generate(version, changelog, rpm=True, src=False)


'''
examples from http://www.manatlan.com/page/py2deb

from py2deb import Py2deb

p=Py2deb("aeff")
p["/usr/lib/python2.5/site-packages"] = ["mymodule.py",]
p.generate("0.1")

p=Py2deb("myprogram")
p["/usr/bin"] = ["myprogram.py|myprogram",]
p.generate("0.2")



from glob import glob
'''
'''
version="0.7.33"
changelog=open("changelog.txt","r").read()

p=Py2deb("fricorder")
p.author="manatlan"
p.mail="manatlan@gmail.com"
p.description="""line one
line two."""
p.url = "http://fricorder.googlecode.com"
p.depends="bash, at, zenity, vlc, python-gtk2, python-glade2, python"
p.license="gpl"
p.section="utils"
p.arch="all"

p["/usr/share/applications"]=["data/fricorder.desktop|fricorder.desktop"]
p["/usr/share/fricorder"]=[i+"|"+i[5:] for i in \
                         glob("data/*.*") + glob("data/templates/*")]
p["/usr/lib/fricorder"]=glob("fricorder/*")+["__init__.py"]
p["/usr/bin"]=["fricorder.py|fricorder"]
p["/usr/share/doc/fricorder"]=["README","COPYING",]

p.generate(version,changelog,rpm=True,src=True)
'''


'''
http://www.manatlan.com/page/py2deb_examples

When we do :

p=Py2deb("packageName")

'p' acts like a dict, where the keys are the destination folder, and the value : a list of existing files.

p["/usr/share/deleteme"]=["file1.py","file2.png",]

(files "file1.py" and "file2.png" should be in the current execution path)

It will generate a "packageName" deb which will install files like that :

    * /usr/share/deleteme/file1.py
    * /usr/share/deleteme/file2.png

Relatives files are installed with their relative path, so something like this :

p["/usr/share/deleteme"]=["file1.py","data/file2.png",]

will produce :

    * /usr/share/deleteme/file1.py
    * /usr/share/deleteme/data/file2.png

It's possible to define files with absolute path too, like that :

p["/usr/share/deleteme"]=["file1.py","/home/me/file2.png",]

which will produce :

    * /usr/share/deleteme/file1.py
    * /usr/share/deleteme/file2.png

But it's possible to rename files, with the 'pipe trick', which can be very handy is some cases :

p["/usr/bin"]=["file1.py|executable",]
p["/usr/share/doc/me"]=["/home/me/mon_cv.htm|cv.html",]

which will produce :

    * /usr/bin/executable (file1.py was renamed as executable)
    * /usr/share/doc/me/cv.html (which was /home/me/mon_cv.htm)

It can be useful to relocate some files too, like that :

p["/usr/share/deleteme"]=["data/images/image.png|image.png","README|doc/french/readme.txt"]

which will produce :

    * /usr/share/deleteme/image.png (image.png is placed at the root path)
    * /usr/share/deleteme/doc/french/readme.txt (README is placed in folders)

At anytime, to see what will be produce, simple 'print p', it will print informations about current package 'p', and list where files will be.

In this case, if the folder 'test' contains file1.py and file2.py

from glob import glob
...
p["/usr/lib/aeff2"] = glob("test/*")
p["/usr/lib/aeff3"] = [i+"|"+i[5:] for i in glob("test/*")]
...
print p

will print :

[...]
/usr/lib/aeff2/test/file1.py
/usr/lib/aeff2/test/file2.py
/usr/lib/aeff3/file1.py (test/file1.py)
/usr/lib/aeff3/file2.py (test/file2.py)
[...]

when a line contains something in '()', it should warn you that the file was renamed/relocated, so the real path of the file is displayed between the '()'.

Just note that the two following commands should produce the same thing :

p["/usr/lib/hello"] = ["file1.png|data/file1.png",]
p["/usr/lib/hello/data"] = ["file1.png",]

something like this : /usr/lib/hello/data/file1.png
'''



'''
http://www.manatlan.com/page/py2deb_configuration

Configuration of a package

from py2deb import Py2deb
p=Py2deb("name")

Only the name of the package is mandatory. But all this attributes are available :

    * description : a textual description, by default "no description"
    * license : a debian license (gpl, lgpl, bsd or artistic), by default "gpl"
    * depends : a list of package/version according debian relationships, by default "" (empty)
    * section : a debian section (see debian sections), by default "utils"
    * arch : a debian architecture (see debian arch ), by default "all"
    * url : url where the package came from, by default ""
    * author : name of the author/packager, by default the env username
    * mail : mail of the author/packager, by default the env username @ hostname

All this attributes can be available via the instance 'p', or can be passed as named arguments in the constructor.
Associate files in a package

Once the instance is created, you must associate files in the package, like that :

p["/usr/bin"]=["file.py",]

'p' acts like a dict, where the keys are the destination folder, and the values : a list of existing files (files! and not folders) in the execution path. Files can be defined as relative or absolute path, but it's not possible to define relative path which contains some ".." tricks. Each file can be renamed with the 'pipe trick', like that :

p["/usr/bin"]=["file.py|executable",]

See more examples
Generation of a package

Simply call the generate() method which is defined like that :

def generate(self,version,changelog="no changelog",rpm=False,src=False)

Only the version is mandatory. But you can pass the changelog to be included in the package here. Put rpm at True if you want a rpm package too (which will simply use 'alien' to convert the deb to rpm). Put src at True if you want a "source package" (source package is a tar.gz "debian source package" which contains a 'debian folder', and can be used to recreate a deb from scratch)

Note that you can't generate a package if you hadn't files in !
Test of a package

At anytime you can see informations about your configuration by simply printing p like that :

print p

Which will display all configuration informations and all included files.

Note it's not a real test, it just try to display what it will try to generate. The generation process can fail if you miss config your files or your informations.
'''

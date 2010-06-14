#!/usr/bin/env python

''' make-deb.sh:
#!/bin/bash

for file in `find infobiotics -type f | egrep -v '(\/\.svn\/)|(\.pyc)|(\.ui)'`
do
    echo "    '$file',"
done
# > files 

python make-deb.py
'''

from thirdparty.py2deb import Py2deb
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
    'bin/infobiotics-dashboard.py|infobiotics-dashboard.py',
]

p['/usr/share/infobiotics-dashboard']=[
    'infobiotics.commons/traits/float_greater_than_zero.py',
    'infobiotics.commons/traits/__init__.py',
    'infobiotics.commons/traits/interfaces.py',
    'infobiotics.commons/traits/int_greater_than_zero.py',
    'infobiotics.commons/traits/float_with_minimum.py',
    'infobiotics.commons/traits/api.py',
    'infobiotics.commons/traits/file_wrapper.py',
    'infobiotics.commons/traits/relative_directory.py',
    'infobiotics.commons/traits/relative_file.py',
    'infobiotics.commons/traits/ui/__init__.py',
    'infobiotics.commons/traits/ui/fixed_file_dialog.py',
    'infobiotics.commons/traits/ui/helpful_controller.py',
    'infobiotics.commons/traits/ui/api.py',
    'infobiotics.commons/traits/ui/qt4/__init__.py',
    'infobiotics.commons/traits/ui/qt4/api.py',
    'infobiotics.commons/traits/ui/qt4/relative_file_editor.py',
    'infobiotics.commons/traits/ui/qt4/relative_directory_editor.py',
    'infobiotics.commons/traits/long_greater_than_zero.py',
    'infobiotics.commons/__init__.py',
    'infobiotics.commons/colours.py',
    'infobiotics.commons/unified_logging.py',
    'infobiotics.commons/lists.py',
    'infobiotics.commons/md5sum.py',
    'infobiotics.commons/api.py',
    'infobiotics.commons/files.py',
    'infobiotics.commons/mayavi.py',
    'infobiotics.commons/strings.py',
    'infobiotics.commons/dicts.py',
    'infobiotics.commons/qt4.py',
    'infobiotics.commons/sequences.py',
    'infobiotics.commons/webbrowsing.py',
    'infobiotics/__init__.py',
    'infobiotics/expect/__init__.py',
    'infobiotics/expect/prism_expect.py',
    'infobiotics/expect/pmodelchecker_expect.py',
    'infobiotics/expect/mc2_expect.py',
    'infobiotics/expect/mcss_expect.py',
    'infobiotics/expect/expect.py',
    'infobiotics/expect/params_expect.py',
    'infobiotics/expect/poptimizer_expect.py',
    'infobiotics/pmodelchecker/mc2/mc2_params_group.py',
    'infobiotics/pmodelchecker/mc2/__init__.py',
    'infobiotics/pmodelchecker/mc2/mc2_experiment_handler.py',
    'infobiotics/pmodelchecker/mc2/mc2_experiment.py',
    'infobiotics/pmodelchecker/mc2/mc2_params.py',
    'infobiotics/pmodelchecker/mc2/api.py',
    'infobiotics/pmodelchecker/mc2/mc2_experiment_progress_handler.py',
    'infobiotics/pmodelchecker/mc2/mc2_mcss_experiment.py',
    'infobiotics/pmodelchecker/mc2/mc2_params_handler.py',
    'infobiotics/pmodelchecker/mc2/mc2_mcss_experiment_group.py',
    'infobiotics/pmodelchecker/__init__.py',
    'infobiotics/pmodelchecker/results/TraitedPrismResults.py',
    'infobiotics/pmodelchecker/results/range_editors_for_dynamic_traits.py',
    'infobiotics/pmodelchecker/api.py',
    'infobiotics/pmodelchecker/pmodelchecker_experiment.py',
    'infobiotics/pmodelchecker/pmodelchecker_params.py',
    'infobiotics/pmodelchecker/model_parameters.py',
    'infobiotics/pmodelchecker/temporal_formulas.py',
    'infobiotics/pmodelchecker/pmodelchecker_params_handler.py',
    'infobiotics/pmodelchecker/prism/__init__.py',
    'infobiotics/pmodelchecker/prism/prism_params.py',
    'infobiotics/pmodelchecker/prism/api.py',
    'infobiotics/pmodelchecker/prism/prism_params_group.py',
    'infobiotics/pmodelchecker/prism/prism_params_handler.py',
    'infobiotics/pmodelchecker/prism/prism_experiment_progress_handler.py',
    'infobiotics/pmodelchecker/prism/prism_experiment_handler.py',
    'infobiotics/pmodelchecker/prism/prism_experiment.py',
    'infobiotics/api.py',
    'infobiotics/common/experiment.py',
    'infobiotics/common/__init__.py',
    'infobiotics/common/_ets_imports.py',
    'infobiotics/common/params.py',
    'infobiotics/common/views.py',
    'infobiotics/common/api.py',
    'infobiotics/common/experiment_handler.py',
    'infobiotics/common/params_handler.py',
    'infobiotics/common/experiment_progress_handler.py',
    'infobiotics/dashboard/__init__.py',
    'infobiotics/dashboard/run.py',
    'infobiotics/dashboard/pmodelchecker/__init__.py',
    'infobiotics/dashboard/pmodelchecker/prism_experiment_dashboard_handler.py',
    'infobiotics/dashboard/pmodelchecker/mc2_experiment_dashboard_handler.py',
    'infobiotics/dashboard/pmodelchecker/ui_plugin.py',
    'infobiotics/dashboard/pmodelchecker/actions.py',
    'infobiotics/dashboard/pmodelchecker/prism_experiment_dashboard_progress_handler.py',
    'infobiotics/dashboard/pmodelchecker/pmodelchecker_action_set.py',
    'infobiotics/dashboard/pmodelchecker/mc2_experiment_dashboard_progress_handler.py',
    'infobiotics/dashboard/pmodelchecker/preferences_page.py',
    'infobiotics/dashboard/api.py',
    'infobiotics/dashboard/app.py',
    'infobiotics/dashboard/mcss/mcss_dashboard_experiment_progress_handler.py',
    'infobiotics/dashboard/mcss/mcss_dashboard_experiment.py',
    'infobiotics/dashboard/mcss/__init__.py',
    'infobiotics/dashboard/mcss/api.py',
    'infobiotics/dashboard/mcss/mcss_dashboard_experiment_handler.py',
    'infobiotics/dashboard/plugins/simulator_results/editor.py',
    'infobiotics/dashboard/plugins/simulator_results/__init__.py',
    'infobiotics/dashboard/plugins/simulator_results/simulator_results.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_plugin.py',
    'infobiotics/dashboard/plugins/simulator_results/main.py',
    'infobiotics/dashboard/plugins/simulator_results/actions.py',
    'infobiotics/dashboard/plugins/simulator_results/icons_rc.py',
    'infobiotics/dashboard/plugins/simulator_results/FromToDoubleSpinBox.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_plots_preview_dialog.py',
    'infobiotics/dashboard/plugins/simulator_results/PlotsListWidget.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_simulation_results_dialog.py',
    'infobiotics/dashboard/plugins/simulator_results/action_set.py',
    'infobiotics/dashboard/plugins/simulator_results/ui_player_control_widget.py',
    'infobiotics/dashboard/plugins/__init__.py',
    'infobiotics/dashboard/plugins/generic_editor.py',
    'infobiotics/dashboard/plugins/pmodelchecker/__init__.py',
    'infobiotics/dashboard/plugins/pmodelchecker/ui_plugin.py',
    'infobiotics/dashboard/plugins/pmodelchecker/actions.py',
    'infobiotics/dashboard/plugins/pmodelchecker/pmodelchecker_action_set.py',
    'infobiotics/dashboard/plugins/pmodelchecker/preferences_page.py',
    'infobiotics/dashboard/plugins/generic_actions.py',
    'infobiotics/dashboard/plugins/progress/experiment_progress_item.py',
    'infobiotics/dashboard/plugins/progress/experiment_queue.py',
    'infobiotics/dashboard/plugins/progress/experiment.py',
    'infobiotics/dashboard/plugins/progress/progress_meter.py',
    'infobiotics/dashboard/plugins/progress/progress_item.py',
    'infobiotics/dashboard/plugins/progress/ui_plugin.py',
    'infobiotics/dashboard/plugins/progress/progress_dialog.py',
    'infobiotics/dashboard/plugins/progress/noninteractive_progress_meter.py',
    'infobiotics/dashboard/plugins/progress/i_progress_meter.py',
    'infobiotics/dashboard/plugins/mcss/__init__.py',
    'infobiotics/dashboard/plugins/mcss/ui_plugin.py',
    'infobiotics/dashboard/plugins/mcss/actions.py',
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
    'infobiotics/dashboard/plugins/poptimizer/action_set.py',
    'infobiotics/dashboard/plugins/generic_action_set.py',
    'infobiotics/dashboard/poptimizer/poptimizer_experiment_dashboard_progress_handler.py',
    'infobiotics/dashboard/poptimizer/__init__.py',
    'infobiotics/dashboard/poptimizer/ui_plugin.py',
    'infobiotics/dashboard/poptimizer/actions.py',
    'infobiotics/dashboard/poptimizer/poptimizer_experiment_dashboard_handler.py',
    'infobiotics/dashboard/poptimizer/action_set.py',
    'infobiotics/mcss/mcss_experiment.py',
    'infobiotics/mcss/__init__.py',
    'infobiotics/mcss/mcss_params.py',
    'infobiotics/mcss/results/__init__.py',
    'infobiotics/mcss/api.py',
    'infobiotics/mcss/mcss_experiment_progress_handler.py',
    'infobiotics/mcss/mcss_params_group.py',
    'infobiotics/mcss/old_mcss_experiment.py',
    'infobiotics/mcss/mcss_experiment_handler.py',
    'infobiotics/mcss/mcss_params_handler.py',
    'infobiotics/poptimizer/poptimizer_experiment_progress_handler.py',
    'infobiotics/poptimizer/__init__.py',
    'infobiotics/poptimizer/api.py',
    'infobiotics/poptimizer/poptimizer_experiment_handler.py',
    'infobiotics/poptimizer/poptimizer_params_handler.py',
    'infobiotics/poptimizer/poptimizer_experiment.py',
    'infobiotics/poptimizer/poptimizer_params_group.py',
    'infobiotics/poptimizer/poptimizer_params.py',

#    'infobiotics/dashboard/images/logo/infobiotics_logo-1.png',
#    'infobiotics/dashboard/images/logo/infobiotics_logo-2.png',
#    'infobiotics/dashboard/images/infobiotics_logo-1.png',
#    'infobiotics/dashboard/images/infobiotics_logo-2.png',
]

p.arch='all'
version=open('VERSION.txt','r').read()
changelog=open('CHANGES.txt','r').read()
p.generate(version, changelog, rpm=False, src=False) #TODO rpm, src


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

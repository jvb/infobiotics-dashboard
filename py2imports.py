'''Explicit imports for modules and packages that not automatically picked up by
modulefinder when running py2app and py2exe, in particular this includes 
Enthought's TraitsUI backend modules that are dynamically loaded.

The infobiotics modules import statements can be generated using the command:

find infobiotics *.py | grep '.py$' | grep -v -E 'setup.py|py2imports.py|.__init__|.svn' | sed 's/\//./g' | sed 's/.py$//' | sed 's/[.]*/    import &/' | grep -v '\._[^_]' | grep -v -E 'infobiotics\.language|infobiotics\.commons\.unused|dashboard\.core\.new|dashboard\.old|mcss\.results\.old|mcss\.results\.tests|mcss\.old'#> py2imports.txt
'''

if False: # guard - py2exe and py2app modulefinder uses lexical analysis so this still works

    # PyQt4
    import sip
    import PyQt4
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from PyQt4 import Qsci
    from PyQt4 import QtNetwork
    # supposed to fix matplotlib SVG icons http://groups.google.com/group/pyinstaller/browse_thread/thread/834bea87c7afcdff 
    # it doesn't as far as I can tell
    from PyQt4 import QtSvg
    from PyQt4 import QtXml
    # maybe this will instead
    import PyQt4.QtXml
    import PyQt4.QtSvg
#    import qt
    import PyQt4._qt

    # progressbar
    import progressbar

    # NumPy
    import numpy
    import numpy.core
    from numpy import *
    from numpy.core import *
    
    # matplotlib
    import matplotlib
    
    # quantities
    import quantities
    from quantities import *
    import quantities.markup # might need a datafile too
    import quantities.units
    from quantities.units import *
    import quantities.quantity
    import quantities.unitquantity
    import quantities.units
    import quantities.units.prefixes
    import quantities.units.substance
    import quantities.units.time
    import quantities.units.volume
    
    # setproctitle
    import setproctitle
    
    # vtk
    import vtk
    import vtk.vtkVersion
    from vtk import *
    from vtk import libvtkCommonPython
    from vtk import libvtkFilteringPython
    from vtk import libvtkGenericFilteringPython
    from vtk import libvtkGeovisPython
    from vtk import libvtkGraphicsPython
    from vtk import libvtkHybridPython
    from vtk import libvtkIOPython
    from vtk import libvtkImagingPython
    from vtk import libvtkInfovisPython
    from vtk import libvtkParallelPython
    from vtk import libvtkRenderingPython
    from vtk import libvtkViewsPython
    from vtk import libvtkVolumeRenderingPython
    from vtk import libvtkWidgetsPython
    
    # traitsbackendqt
    from pyface.ui.qt4 import about_dialog, application_window, clipboard, confirmation_dialog, dialog, directory_dialog, file_dialog, gui, heading_text, image_cache, image_resource, init, message_dialog, progress_dialog, python_editor, python_shell, resource_manager, splash_screen, split_widget, system_metrics, widget, window
    from pyface.ui.qt4.action import action_item, menu_manager, menu_bar_manager, status_bar_manager, tool_bar_manager
    from pyface.timer import do_later
    from pyface.ui.qt4.timer import do_later
    from pyface.ui.qt4.workbench import editor, split_tab_widget, view, workbench_window_layout
    import traitsui.qt4
    
    # envisage
    from envisage.ui.workbench.action import api
    import envisage.plugins.ipython_shell.actions
    import envisage.plugins.ipython_shell.actions.ipython_shell_actions
    import envisage.plugins.refresh_code.actions
    import envisage.plugins.remote_editor.actions
    import envisage.plugins.text_editor.actions
    
    # TVTK
    import tvtk.plugins.scene.ui.actions # Envisage actions

    import tvtk
    import tvtk.vtk_module
    import tvtk.pyface.ui.qt4.init
    import tvtk.pyface.ui.qt4
    from tvtk.pyface.ui.qt4.scene_editor import *

    import tvtk.tvtk_classes # unzipped in py2exe/py2app.sh
    import tvtk.tvtk_classes.vtk_version
    from tvtk.tvtk_classes import * 

    # infobiotics-dashboard
    '''Generated with:
    find infobiotics *.py | grep '.py$' | grep -v -E 'setup.py|py2imports.py|.__init__|.svn' | sed 's/\//./g' | sed 's/.py$//' | sed 's/[.]*/    import &/' | grep -v '\._[^_]' | grep -v -E 'infobiotics\.language|infobiotics\.commons\.unused|dashboard\.core\.new|dashboard\.old|mcss\.results\.old|mcss\.results\.tests|mcss\.old'#> py2imports.txt
    
    Explanation:
    find infobiotics *.py # find files and directories including *.py under (and including) infobiotics 
    grep '.py$' # exclude directories and .pyc files
    grep -v -E 'setup.py|py2imports.py|.__init__|.svn' # exclude setup.py, py2imports.py, __init__.py and files in .svn directories
    sed 's/\//./g' # replace forward slashes with dots 
    sed 's/.py$//' # remove .py extensions from end of line
    sed 's/[.]*/    import &/' # prepend a 4 spaces and an import statement
    grep -v '\._[^_]' # remove file names starting with an underscore but not 2 underscores
    ...
    '''    
    import infobiotics.core.traits_.model_file
    import infobiotics.core.traits_.params_relative_directory
    import infobiotics.core.traits_.params_relative_file
    import infobiotics.core.experiment
    import infobiotics.core.params
    import infobiotics.core.params_preferences
    import infobiotics.core.views
    import infobiotics.core.api
    import infobiotics.core.experiment_handler
    import infobiotics.core.params_handler
    import infobiotics.core.experiment_progress_handler
    import infobiotics.pmodelchecker.mc2.mc2_params_group
    import infobiotics.pmodelchecker.mc2.mc2_experiment
    import infobiotics.pmodelchecker.mc2.mc2_params
    import infobiotics.pmodelchecker.mc2.mc2_mcss_experiment
    import infobiotics.pmodelchecker.mc2.mc2_params_handler
    import infobiotics.pmodelchecker.mc2.mc2_mcss_experiment_group
    import infobiotics.pmodelchecker.mc2.mc2_preferences
    import infobiotics.pmodelchecker.pmodelchecker_experiment_handler
    import infobiotics.pmodelchecker.pmodelchecker_experiment
    import infobiotics.pmodelchecker.pmodelchecker_params
    import infobiotics.pmodelchecker.model_parameters
    import infobiotics.pmodelchecker.pmodelchecker_results
    import infobiotics.pmodelchecker.pmodelchecker_preferences
    import infobiotics.pmodelchecker.temporal_formulas
    import infobiotics.pmodelchecker.pmodelchecker_params_handler
    import infobiotics.pmodelchecker.prism.prism_params
    import infobiotics.pmodelchecker.prism.prism_params_group
    import infobiotics.pmodelchecker.prism.prism_preferences
    import infobiotics.pmodelchecker.prism.prism_params_handler
    import infobiotics.pmodelchecker.prism.prism_experiment
    import infobiotics.api
    import infobiotics.commons.traits_.float_greater_than_zero
    import infobiotics.commons.traits_.interfaces
    import infobiotics.commons.traits_.int_greater_than_zero
    import infobiotics.commons.traits_.api
    import infobiotics.commons.traits_.file_wrapper
    import infobiotics.commons.traits_.relative_directory
    import infobiotics.commons.traits_.percentage
    import infobiotics.commons.traits_.relative_file
    import infobiotics.commons.traits_.ui.fixed_file_dialog
    import infobiotics.commons.traits_.ui.helpful_controller
    import infobiotics.commons.traits_.ui.api
    import infobiotics.commons.traits_.ui.values_for_enum_editor
    import infobiotics.commons.traits_.ui.key_bindings
    import infobiotics.commons.traits_.ui.qt4.api
    import infobiotics.commons.traits_.ui.qt4.matplotlib_figure_editor
    import infobiotics.commons.traits_.ui.qt4.cancellable_progress_editor
    import infobiotics.commons.traits_.ui.qt4.relative_file_editor
    import infobiotics.commons.traits_.ui.qt4.progress_editor
    import infobiotics.commons.traits_.ui.qt4.relative_directory_editor
    import infobiotics.commons.traits_.long_greater_than_zero
    import infobiotics.commons.traits_.tests.test_relative_directory_and_params_relative_file.test_relative_directory_and_params_relative_file
    import infobiotics.commons.quantities.units.concentration
    import infobiotics.commons.quantities.units.length
    import infobiotics.commons.quantities.units.calculators
    import infobiotics.commons.quantities.units.volume
    import infobiotics.commons.quantities.units.substance
    import infobiotics.commons.quantities.units.time
    import infobiotics.commons.quantities.api
    import infobiotics.commons.quantities.traits_ui_converters
    import infobiotics.commons.colours
    import infobiotics.commons.unified_logging
    import infobiotics.commons.md5sum
    import infobiotics.commons.counter2
    import infobiotics.commons.api
    import infobiotics.commons.files
    import infobiotics.commons.metaclasses.noconflict
    import infobiotics.commons.mayavi_
    import infobiotics.commons.strings
    import infobiotics.commons.dicts
    import infobiotics.commons.qt4
    import infobiotics.commons.matplotlib.draggable_legend
    import infobiotics.commons.matplotlib.matplotlib_figure_size
    import infobiotics.commons.pyqt4.list_widget
    import infobiotics.commons.pyqt4.actions
    import infobiotics.commons.orderedset
    import infobiotics.commons.counter
    import infobiotics.commons.sequences
    import infobiotics.commons.ordereddict
    import infobiotics.commons.multiset
    import infobiotics.commons.names
    import infobiotics.commons.descriptors
    import infobiotics.commons.webbrowsing
    import infobiotics.preferences
    import infobiotics.dashboard.core.ui_plugin
    import infobiotics.dashboard.core.actions
    import infobiotics.dashboard.core.dashboard_experiment_handler
    import infobiotics.dashboard.core.dashboard_experiment
    import infobiotics.dashboard.core.dashboard_experiment_editor
    import infobiotics.dashboard.core.action_set
    import infobiotics.dashboard.core.preferences_page
    import infobiotics.dashboard.run
    import infobiotics.dashboard.pmodelchecker.mc2_dashboard_experiment_handler
    import infobiotics.dashboard.pmodelchecker.editor
    import infobiotics.dashboard.pmodelchecker.prism_dashboard_experiment
    import infobiotics.dashboard.pmodelchecker.ui_plugin
    import infobiotics.dashboard.pmodelchecker.actions
    import infobiotics.dashboard.pmodelchecker.commons
    import infobiotics.dashboard.pmodelchecker.prism_dashboard_experiment_handler
    import infobiotics.dashboard.pmodelchecker.mc2_dashboard_experiment
    import infobiotics.dashboard.pmodelchecker.action_set
    import infobiotics.dashboard.pmodelchecker.preferences_page
    import infobiotics.dashboard.api
    import infobiotics.dashboard.app
    import infobiotics.dashboard.mcss.mcss_dashboard_experiment
    import infobiotics.dashboard.mcss.results.editor
    import infobiotics.dashboard.mcss.results.ui_plugin
    import infobiotics.dashboard.mcss.results.actions
    import infobiotics.dashboard.mcss.results.action_set
    import infobiotics.dashboard.mcss.ui_plugin
    import infobiotics.dashboard.mcss.actions
    import infobiotics.dashboard.mcss.mcss_dashboard_experiment_handler
    import infobiotics.dashboard.mcss.action_set
    import infobiotics.dashboard.poptimizer.ui_plugin
    import infobiotics.dashboard.poptimizer.actions
    import infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment_handler
    import infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment
    import infobiotics.dashboard.poptimizer.action_set
    import infobiotics.__version__
    import infobiotics.thirdparty.which
    import infobiotics.thirdparty.statistics
#    import infobiotics.mcsscmaes.mcsscmaes_params_group
#    import infobiotics.mcsscmaes.mcsscmaes_preferences
#    import infobiotics.mcsscmaes.api
#    import infobiotics.mcsscmaes.mcsscmaes_experiment_progress_handler
#    import infobiotics.mcsscmaes.mcsscmaes_experiment_handler
#    import infobiotics.mcsscmaes.mcsscmaes_params_handler
#    import infobiotics.mcsscmaes.mcsscmaes_experiment
#    import infobiotics.mcsscmaes.mcsscmaes_params
    import infobiotics.mcss.mcss_experiment
    import infobiotics.mcss.mcss_params
    import infobiotics.mcss.results.axes_order_traits
    import infobiotics.mcss.results.spatial_plots
    import infobiotics.mcss.results.compartments_list_widget
    import infobiotics.mcss.results.compartment
    import infobiotics.mcss.results.run
    import infobiotics.mcss.results.statistics
    import infobiotics.mcss.results.surfaces_widget
    import infobiotics.mcss.results.species
    import infobiotics.mcss.results.histograms
    import infobiotics.mcss.results.simulation_list_widget_item
    import infobiotics.mcss.results.movie
    import infobiotics.mcss.results.icons_rc
    import infobiotics.mcss.results.FromToDoubleSpinBox
    import infobiotics.mcss.results.ui_plots_preview_dialog
    import infobiotics.mcss.results.driver
    import infobiotics.mcss.results.table
    import infobiotics.mcss.results.timeseries
    import infobiotics.mcss.results.PlotsListWidget
    import infobiotics.mcss.results.mcss_results
    import infobiotics.mcss.results.timeseries_plot
#    import infobiotics.mcss.results.oregonator_movie
    import infobiotics.mcss.results.ui_mcss_results_widget
    import infobiotics.mcss.results.simulation
#    import infobiotics.mcss.results.combined_surfaces
    import infobiotics.mcss.results.mcss_results_widget
    import infobiotics.mcss.results.ui_player_control_widget
    import infobiotics.mcss.mcss_params_group
    import infobiotics.mcss.mcss_preferences
    import infobiotics.mcss.mcss_experiment_handler
    import infobiotics.mcss.mcss_params_handler
    import infobiotics.poptimizer.poptimizer_experiment_handler
    import infobiotics.poptimizer.poptimizer_params_handler
    import infobiotics.poptimizer.poptimizer_experiment
    import infobiotics.poptimizer.poptimizer_params_group
    import infobiotics.poptimizer.poptimizer_results
    import infobiotics.poptimizer.poptimizer_preferences
    import infobiotics.poptimizer.poptimizer_params

'''Explicit imports for modules and packages that not automatically picked up by
modulefinder when running py2app and py2exe, in particular this includes 
Enthought's TraitsUI backend modules that are dynamically loaded.

The infobiotics modules import statements can be generated using the command:
find infobiotics *.py | grep '.py$' | grep -v -E 'setup.py|py2imports.py|.__init__|.svn' | sed 's/\//./g' | sed 's/.py$//' | sed 's/[.]*/    import &/' | grep -v '\._[^_]'
#> py2imports.txt
but some files have been excluded manually with comments. 
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
    from enthought.pyface.ui.qt4 import about_dialog, application_window, clipboard, confirmation_dialog, dialog, directory_dialog, file_dialog, gui, heading_text, image_cache, image_resource, init, message_dialog, progress_dialog, python_editor, python_shell, resource_manager, splash_screen, split_widget, system_metrics, widget, window
    from enthought.pyface.ui.qt4.action import action_item, menu_manager, menu_bar_manager, status_bar_manager, tool_bar_manager
    from enthought.pyface.timer import do_later
    from enthought.pyface.ui.qt4.timer import do_later
    from enthought.pyface.ui.qt4.workbench import editor, split_tab_widget, view, workbench_window_layout
    import enthought.traits.ui.qt4
    
    # envisage
    from enthought.envisage.ui.workbench.action import api
    import enthought.plugins.ipython_shell.actions
    import enthought.plugins.ipython_shell.actions.ipython_shell_actions
    import enthought.plugins.refresh_code.actions
    import enthought.plugins.remote_editor.actions
    import enthought.plugins.text_editor.actions
    
    # TVTK
    import enthought.tvtk.plugins.scene.ui.actions # Envisage actions

    import enthought.tvtk
    import enthought.tvtk.vtk_module
    import enthought.tvtk.pyface.ui.qt4.init
    import enthought.tvtk.pyface.ui.qt4
    from enthought.tvtk.pyface.ui.qt4.scene_editor import *

    import enthought.tvtk.tvtk_classes # unzipped in py2exe/py2app.sh
    import enthought.tvtk.tvtk_classes.vtk_version
    from enthought.tvtk.tvtk_classes import * 

    # infobiotics-dashboard
#    find infobiotics *.py | grep '.py$' | grep -v -E 'setup.py|py2imports.py|.__init__|.svn' | sed 's/\//./g' | sed 's/.py$//' | sed 's/[.]*/    import &/' | grep -v '\._[^_]'
    '''
    find infobiotics *.py # find files and directories including *.py under (and including) infobiotics 
    grep '.py$' # exclude directories and .pyc files
    grep -v -E 'setup.py|py2imports.py|.__init__|.svn' # exclude setup.py, py2imports.py, __init__.py and files in .svn directories
    sed 's/\//./g' # replace forward slashes with dots 
    sed 's/.py$//' # remove .py extensions from end of line
    sed 's/[.]*/    import &/' # prepend a 4 spaces and an import statement
    grep -v '\._[^_]' # remove file names starting with an underscore but not 2 underscores
    '''    
    # use this command to create the list of infobiotics files below
    import infobiotics.core.traits.model_file
    import infobiotics.core.traits.params_relative_directory
    import infobiotics.core.traits.params_relative_file
    import infobiotics.core.experiment
    import infobiotics.core.params
    import infobiotics.core.params_preferences
    import infobiotics.core.views
    import infobiotics.core.api
    import infobiotics.core.experiment_handler
    import infobiotics.core.params_handler
    import infobiotics.core.experiment_progress_handler
#    import infobiotics.core.winpexpect
#    import infobiotics.language.dependency_graphs
#    import infobiotics.language.partial_propensities_fixed
#    import infobiotics.language.module1
#    import infobiotics.language.TODO
#    import infobiotics.language.partial_propensities
#    import infobiotics.language.species
#    import infobiotics.language.module_introspection.ply
#    import infobiotics.language.module_introspection.ply_importing_module
#    import infobiotics.language.api
#    import infobiotics.language.partial_propensities_backup
#    import infobiotics.language.sbml
#    import infobiotics.language.old.lat
#    import infobiotics.language.old.rule
#    import infobiotics.language.old.lpp
#    import infobiotics.language.old.plb
#    import infobiotics.language.old.sps
#    import infobiotics.language.old.IFFL
#    import infobiotics.language.reactions
#    import infobiotics.language.compartmentmixin
#    import infobiotics.language.partial
#    import infobiotics.language.example
#    import infobiotics.language.config
#    import infobiotics.language.model
#    import infobiotics.language.PAO1
#    import infobiotics.language.metacompartment
#    import infobiotics.language.examples.todo
#    import infobiotics.language.compartments
#    import infobiotics.language.volumes
#    import infobiotics.language.lexing.lexer4
#    import infobiotics.language.lexing.lexer
#    import infobiotics.language.lexing.lexer3
#    import infobiotics.language.lexing.lpp_editor
#    import infobiotics.language.lexing.qt_lexer
#    import infobiotics.language.lexing.lexer2
#    import infobiotics.language.lexing.lpp_editor3
#    import infobiotics.language.lexing.lpp_editor2
#    import infobiotics.language.lexing.sps_lexer
#    import infobiotics.language.tests.test_reaction_rate_determination
#    import infobiotics.language.tests.todo.declarative_properties
#    import infobiotics.language.tests.todo.eval_model_string
#    import infobiotics.language.tests.todo.modules_with_modules
#    import infobiotics.language.tests.todo.single_inheritance
#    import infobiotics.language.tests.todo.process
#    import infobiotics.language.tests.todo.compartment
#    import infobiotics.language.tests.todo.concentrations
#    import infobiotics.language.tests.todo.species
#    import infobiotics.language.tests.todo.test_compartment_metadata
#    import infobiotics.language.tests.todo.distributions_for_rates
#    import infobiotics.language.tests.todo.initial_multisets
#    import infobiotics.language.tests.todo.module_decorator
#    import infobiotics.language.tests.todo.export_iml
#    import infobiotics.language.tests.todo.sequences
#    import infobiotics.language.tests.todo.generic
#    import infobiotics.language.tests.todo.export_sbml
#    import infobiotics.language.tests.todo.modules_as_functions
#    import infobiotics.language.tests.todo.multiple_inheritance
#    import infobiotics.language.tests.todo.compartments
#    import infobiotics.language.tests.todo.distributions_for_amounts
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
    import infobiotics.commons.traits.float_greater_than_zero
    import infobiotics.commons.traits.interfaces
    import infobiotics.commons.traits.int_greater_than_zero
    import infobiotics.commons.traits.api
    import infobiotics.commons.traits.file_wrapper
    import infobiotics.commons.traits.relative_directory
    import infobiotics.commons.traits.percentage
    import infobiotics.commons.traits.relative_file
    import infobiotics.commons.traits.ui.fixed_file_dialog
    import infobiotics.commons.traits.ui.helpful_controller
    import infobiotics.commons.traits.ui.api
    import infobiotics.commons.traits.ui.values_for_enum_editor
    import infobiotics.commons.traits.ui.key_bindings
    import infobiotics.commons.traits.ui.qt4.api
    import infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor
    import infobiotics.commons.traits.ui.qt4.cancellable_progress_editor
    import infobiotics.commons.traits.ui.qt4.relative_file_editor
    import infobiotics.commons.traits.ui.qt4.progress_editor
    import infobiotics.commons.traits.ui.qt4.relative_directory_editor
    import infobiotics.commons.traits.long_greater_than_zero
    import infobiotics.commons.traits.tests.test_relative_directory_and_params_relative_file.test_relative_directory_and_params_relative_file
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
    import infobiotics.commons.mayavi
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
#    import infobiotics.commons.unused.silence
    import infobiotics.commons.multiset
    import infobiotics.commons.names
    import infobiotics.commons.descriptors
    import infobiotics.commons.webbrowsing
    import infobiotics.preferences
#    import infobiotics.dashboard.core.new.default_action_set
#    import infobiotics.dashboard.core.new.generic_actions
#    import infobiotics.dashboard.core.new.plugin
#    import infobiotics.dashboard.core.new.actions.open_action
#    import infobiotics.dashboard.core.new.actions.close_all
#    import infobiotics.dashboard.core.new.actions.save_as_action
#    import infobiotics.dashboard.core.new.actions.example_action
#    import infobiotics.dashboard.core.new.actions.close_action
#    import infobiotics.dashboard.core.new.actions.python_module_action
#    import infobiotics.dashboard.core.new.actions.open_python_module_action
#    import infobiotics.dashboard.core.new.actions.new_window_action
#    import infobiotics.dashboard.core.new.actions.untitled_text_file_action
#    import infobiotics.dashboard.core.new.actions.about_action
#    import infobiotics.dashboard.core.new.actions.open_text_file_action
#    import infobiotics.dashboard.core.new.actions.save_action
#    import infobiotics.dashboard.core.new.actions.exit_action
#    import infobiotics.dashboard.core.new.actions.new_editor_action
#    import infobiotics.dashboard.core.new.application
#    import infobiotics.dashboard.core.new.editors.code_file_editor
#    import infobiotics.dashboard.core.new.editors.api
#    import infobiotics.dashboard.core.new.editors.text_file_editor
#    import infobiotics.dashboard.core.new.editors.abstract_file_editor
#    import infobiotics.dashboard.core.new.editors.python_module_editor
#    import infobiotics.dashboard.core.new.generic_action_set
#    import infobiotics.dashboard.core.new.core_action_set
    import infobiotics.dashboard.core.ui_plugin
    import infobiotics.dashboard.core.actions
    import infobiotics.dashboard.core.has_infobiotics_dashboard_workbench_application
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
#    import infobiotics.dashboard.old.file_editors.abstract_file_editor_action_set
#    import infobiotics.dashboard.old.file_editors.test_app_run
#    import infobiotics.dashboard.old.file_editors.api
#    import infobiotics.dashboard.old.file_editors.actions
#    import infobiotics.dashboard.old.file_editors.plugin
#    import infobiotics.dashboard.old.file_editors.editors.file_editor_handler
#    import infobiotics.dashboard.old.file_editors.editors.text_file_editor
#    import infobiotics.dashboard.old.file_editors.editors.python_module_editor_handler
#    import infobiotics.dashboard.old.file_editors.editors.abstract_file_editor
#    import infobiotics.dashboard.old.file_editors.editors.python_module_editor
#    import infobiotics.dashboard.old.file_editors.action_set
#    import infobiotics.dashboard.old.text_editor.api
#    import infobiotics.dashboard.old.text_editor.actions
#    import infobiotics.dashboard.old.text_editor.text_editor_plugin
#    import infobiotics.dashboard.old.text_editor.editor.text_editor_handler
#    import infobiotics.dashboard.old.text_editor.editor.text_editor
#    import infobiotics.dashboard.old.text_editor.text_editor_action_set
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
    import infobiotics.mcsscmaes.mcsscmaes_params_group
    import infobiotics.mcsscmaes.mcsscmaes_preferences
    import infobiotics.mcsscmaes.api
    import infobiotics.mcsscmaes.mcsscmaes_experiment_progress_handler
    import infobiotics.mcsscmaes.mcsscmaes_experiment_handler
    import infobiotics.mcsscmaes.mcsscmaes_params_handler
    import infobiotics.mcsscmaes.mcsscmaes_experiment
    import infobiotics.mcsscmaes.mcsscmaes_params
    import infobiotics.mcss.mcss_experiment
    import infobiotics.mcss.mcss_params
    import infobiotics.mcss.results.axes_order_traits
    import infobiotics.mcss.results.spatial_plots
    import infobiotics.mcss.results.compartments_list_widget
    import infobiotics.mcss.results.compartment
    import infobiotics.mcss.results.run
#    import infobiotics.mcss.results.ui_mcss_results_widget-backup
    import infobiotics.mcss.results.surfaces_widget
    import infobiotics.mcss.results.species
    import infobiotics.mcss.results.histograms
    import infobiotics.mcss.results.simulation_list_widget_item
    import infobiotics.mcss.results.movie
    import infobiotics.mcss.results.icons_rc
    import infobiotics.mcss.results.FromToDoubleSpinBox
    import infobiotics.mcss.results.ui_plots_preview_dialog
    import infobiotics.mcss.results.driver
#    import infobiotics.mcss.results.old.mcss_results_widget_traited.mcss_results_editors
#    import infobiotics.mcss.results.old.mcss_results_widget_traited.mcss_results_plots
#    import infobiotics.mcss.results.old.mcss_results_widget_traited.mcss_results_views
#    import infobiotics.mcss.results.old.mcss_results_widget_traited.mcss_results_handler
#    import infobiotics.mcss.results.old.mcss_results_widget_traited.mcss_results_actions
#    import infobiotics.mcss.results.old.mcss_results_widget_traited.mcss_results
#    import infobiotics.mcss.results.old.mcss_results_widget_traited.mcss_results_groups
#    import infobiotics.mcss.results.old.ideas
    import infobiotics.mcss.results.table
    import infobiotics.mcss.results.timeseries
    import infobiotics.mcss.results.PlotsListWidget
    import infobiotics.mcss.results.ui_simulation_results_dialog
    import infobiotics.mcss.results.mcss_results
    import infobiotics.mcss.results.timeseries_plot
    import infobiotics.mcss.results.ui_mcss_results_widget
#    import infobiotics.mcss.results.adapted_wigner
    import infobiotics.mcss.results.simulation
#    import infobiotics.mcss.results.combined_surfaces
    import infobiotics.mcss.results.mcss_results_widget
#    import infobiotics.mcss.results.tests.time_get_functions_over_runs
#    import infobiotics.mcss.results.tests.test_mcss_results
#    import infobiotics.mcss.results.tests.time_functions_of_values_over_axis
#    import infobiotics.mcss.results.tests.test_mcss_results_widget
#    import infobiotics.mcss.results.tests.mcss_postprocess
    import infobiotics.mcss.results.ui_player_control_widget
    import infobiotics.mcss.mcss_params_group
#    import infobiotics.mcss.old.mcss_experiment
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

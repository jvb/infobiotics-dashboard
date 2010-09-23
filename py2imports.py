'''
Explicit imports for modules and packages that not automatically picked up by
modulefinder when running py2app and py2exe, in particular this includes 
Enthought's TraitsUI backend modules that are dynamically loaded.

The infobiotics modules import statements can be generated using the command:
find infobiotics *.py | grep '.py$' | grep -v -E 'setup.py|py2imports.py|.__init__|.svn' | sed 's/\//./g' | sed 's/.py$//' | sed 's/[.]*/    import &/' | grep -v '\._[^_]'

'''

if False: # guard
    # py2exe and py2app modulefinder uses lexical analysis so this still works

    import sip
    import PyQt4
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from PyQt4 import Qsci
    from PyQt4 import QtNetwork
    from PyQt4 import QtXml # supposed to fix matplotlib SVG icons http://groups.google.com/group/pyinstaller/browse_thread/thread/834bea87c7afcdff # it doesn't as far as I can tell
    from PyQt4 import QtSvg
    
    import numpy
    
    import matplotlib
    
    import vtk
    
    import enthought.traits.ui.qt4
    
    from enthought.pyface.ui.qt4.action import action_item, menu_manager, menu_bar_manager, status_bar_manager, tool_bar_manager
    
    import enthought.tvtk.vtk_module
    import enthought.tvtk.pyface.ui.qt4.init
    import enthought.tvtk.pyface.ui.qt4
    from enthought.tvtk.pyface.ui.qt4.scene_editor import *
    
    from enthought.pyface.ui.qt4 import about_dialog, application_window, clipboard, confirmation_dialog, dialog, directory_dialog, file_dialog, gui, heading_text, image_cache, image_resource, init, message_dialog, progress_dialog, python_editor, python_shell, resource_manager, splash_screen, split_widget, system_metrics, widget, window
    from enthought.pyface.ui.qt4.workbench import editor, split_tab_widget, view, workbench_window_layout
    
    from enthought.envisage.ui.workbench.action import api
    
    import enthought.plugins.ipython_shell.actions
    import enthought.plugins.ipython_shell.actions.ipython_shell_actions
    import enthought.plugins.refresh_code.actions
    import enthought.plugins.remote_editor.actions
    import enthought.plugins.text_editor.actions
    import enthought.tvtk.plugins.scene.ui.actions

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
    import infobiotics.language.lat
    import infobiotics.language.decorators
    import infobiotics.language.lexer4
    import infobiotics.language.rule
    import infobiotics.language.lexer
    import infobiotics.language.lexer3
    import infobiotics.language.api
    import infobiotics.language.modules
    import infobiotics.language.lpp
    import infobiotics.language.plb
    import infobiotics.language.sps
    import infobiotics.language.lexer2
    import infobiotics.language.IFFL
    import infobiotics.language.lpp_editor3
    import infobiotics.language.lpp_editor2
    import infobiotics.language.sps_lexer
    import infobiotics.pmodelchecker.mc2.mc2_params_group
    import infobiotics.pmodelchecker.mc2.mc2_experiment_handler
    import infobiotics.pmodelchecker.mc2.mc2_experiment
    import infobiotics.pmodelchecker.mc2.mc2_params
    import infobiotics.pmodelchecker.mc2.api
    import infobiotics.pmodelchecker.mc2.mc2_experiment_progress_handler
    import infobiotics.pmodelchecker.mc2.mc2_mcss_experiment
    import infobiotics.pmodelchecker.mc2.mc2_params_handler
    import infobiotics.pmodelchecker.mc2.mc2_mcss_experiment_group
    import infobiotics.pmodelchecker.pmodelchecker_experiment_handler
    import infobiotics.pmodelchecker.api
    import infobiotics.pmodelchecker.pmodelchecker_experiment
    import infobiotics.pmodelchecker.pmodelchecker_params
    import infobiotics.pmodelchecker.model_parameters
    import infobiotics.pmodelchecker.pmodelchecker_results
    import infobiotics.pmodelchecker.pmodelchecker_preferences
    import infobiotics.pmodelchecker.temporal_formulas
    import infobiotics.pmodelchecker.pmodelchecker_params_handler
    import infobiotics.pmodelchecker.prism.prism_params
    import infobiotics.pmodelchecker.prism.api
    import infobiotics.pmodelchecker.prism.prism_params_group
    import infobiotics.pmodelchecker.prism.prism_params_handler
    import infobiotics.pmodelchecker.prism.prism_experiment_progress_handler
    import infobiotics.pmodelchecker.prism.prism_experiment_handler
    import infobiotics.pmodelchecker.prism.prism_experiment
    import infobiotics.api
    import infobiotics.commons.traits.float_greater_than_zero
    import infobiotics.commons.traits.interfaces
    import infobiotics.commons.traits.int_greater_than_zero
    import infobiotics.commons.traits.float_with_minimum
    import infobiotics.commons.traits.api
    import infobiotics.commons.traits.file_wrapper
    import infobiotics.commons.traits.relative_directory
    import infobiotics.commons.traits.relative_file
    import infobiotics.commons.traits.ui.fixed_file_dialog
    import infobiotics.commons.traits.ui.helpful_controller
    import infobiotics.commons.traits.ui.api
    import infobiotics.commons.traits.ui.key_bindings
    import infobiotics.commons.traits.ui.qt4.api
    import infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor
    import infobiotics.commons.traits.ui.qt4.cancellable_progress_editor
    import infobiotics.commons.traits.ui.qt4.relative_file_editor
    import infobiotics.commons.traits.ui.qt4.relative_directory_editor
    import infobiotics.commons.traits.long_greater_than_zero
    import infobiotics.commons.colours
    import infobiotics.commons.unified_logging
    import infobiotics.commons.md5sum
    import infobiotics.commons.api
    import infobiotics.commons.files
    import infobiotics.commons.mayavi
    import infobiotics.commons.strings
    import infobiotics.commons.dicts
    import infobiotics.commons.qt4
    import infobiotics.commons.matplotlib.draggable_legend
    import infobiotics.commons.matplotlib.matplotlib_figure_size
    import infobiotics.commons.pyqt4.list_widget
    import infobiotics.commons.pyqt4.actions
    import infobiotics.commons.sequences
    import infobiotics.commons.webbrowsing
    import infobiotics.preferences
    import infobiotics.dashboard.core.dashboard_experiment_progress_handler
    import infobiotics.dashboard.core.api
    import infobiotics.dashboard.core.has_infobiotics_dashboard_workbench_application
    import infobiotics.dashboard.core.dashboard_experiment_handler
    import infobiotics.dashboard.core.dashboard_experiment
    import infobiotics.dashboard.run
    import infobiotics.dashboard.pmodelchecker.mc2_dashboard_experiment_handler
    import infobiotics.dashboard.pmodelchecker.prism_dashboard_experiment
    import infobiotics.dashboard.pmodelchecker.prism_dashboard_experiment_progress_handler
    import infobiotics.dashboard.pmodelchecker.api
    import infobiotics.dashboard.pmodelchecker.commons
    import infobiotics.dashboard.pmodelchecker.mc2_dashboard_experiment_progress_handler
    import infobiotics.dashboard.pmodelchecker.prism_dashboard_experiment_handler
    import infobiotics.dashboard.pmodelchecker.mc2_dashboard_experiment
    import infobiotics.dashboard.api
    import infobiotics.dashboard.app
    import infobiotics.dashboard.mcss.mcss_dashboard_experiment_progress_handler
    import infobiotics.dashboard.mcss.mcss_dashboard_experiment
    import infobiotics.dashboard.mcss.api
    import infobiotics.dashboard.mcss.mcss_dashboard_experiment_handler
    import infobiotics.dashboard.plugins.simulator_results.axes_order_traits
    import infobiotics.dashboard.plugins.simulator_results.editor
    import infobiotics.dashboard.plugins.simulator_results.compartments_list_widget
    import infobiotics.dashboard.plugins.simulator_results.simulator_results
    import infobiotics.dashboard.plugins.simulator_results.axes_order_qt
    import infobiotics.dashboard.plugins.simulator_results.structure
    import infobiotics.dashboard.plugins.simulator_results.QListWidget_insert
    import infobiotics.dashboard.plugins.simulator_results.histograms2.SimulationDatasets
    import infobiotics.dashboard.plugins.simulator_results.histograms2.EnhancedListWidget
    import infobiotics.dashboard.plugins.simulator_results.histograms2.Workbench
    import infobiotics.dashboard.plugins.simulator_results.histograms2.md5sum
    import infobiotics.dashboard.plugins.simulator_results.histograms2.functions
    import infobiotics.dashboard.plugins.simulator_results.histograms2.actions
    import infobiotics.dashboard.plugins.simulator_results.histograms2.HistogramWidget
    import infobiotics.dashboard.plugins.simulator_results.histograms2.SimulationWidgets
    import infobiotics.dashboard.plugins.simulator_results.test_get_results_for_functions_over_axes
    import infobiotics.dashboard.plugins.simulator_results.ui_plugin
    import infobiotics.dashboard.plugins.simulator_results.actions
    import infobiotics.dashboard.plugins.simulator_results.icons_rc
    import infobiotics.dashboard.plugins.simulator_results.FromToDoubleSpinBox
    import infobiotics.dashboard.plugins.simulator_results.ui_plots_preview_dialog
    import infobiotics.dashboard.plugins.simulator_results.npz_info
    import infobiotics.dashboard.plugins.simulator_results.PlotsListWidget
    import infobiotics.dashboard.plugins.simulator_results.ui_simulation_results_dialog
    import infobiotics.dashboard.plugins.simulator_results.test_generic_function
    import infobiotics.dashboard.plugins.simulator_results.histograms.qt_mpl_bars
    import infobiotics.dashboard.plugins.simulator_results.histograms.polys3d_demo
    import infobiotics.dashboard.plugins.simulator_results.histograms.qt_mpl_bars_histogram_simulation
    import infobiotics.dashboard.plugins.simulator_results.histograms.hist3d_demo
    import infobiotics.dashboard.plugins.simulator_results.action_set
    import infobiotics.dashboard.plugins.simulator_results.ui_player_control_widget
    import infobiotics.dashboard.plugins.core.ui_plugin
    import infobiotics.dashboard.plugins.core.actions
    import infobiotics.dashboard.plugins.core.action_set
    import infobiotics.dashboard.plugins.core.preferences_page
    import infobiotics.dashboard.plugins.pmodelchecker.editor
    import infobiotics.dashboard.plugins.pmodelchecker.ui_plugin
    import infobiotics.dashboard.plugins.pmodelchecker.actions
    import infobiotics.dashboard.plugins.pmodelchecker.action_set
    import infobiotics.dashboard.plugins.pmodelchecker.preferences_page
    import infobiotics.dashboard.plugins.file_editors.abstract_file_editor_action_set
    import infobiotics.dashboard.plugins.file_editors.test_app_run
    import infobiotics.dashboard.plugins.file_editors.api
    import infobiotics.dashboard.plugins.file_editors.actions
    import infobiotics.dashboard.plugins.file_editors.plugin
    import infobiotics.dashboard.plugins.file_editors.editors.file_editor_handler
    import infobiotics.dashboard.plugins.file_editors.editors.text_file_editor
    import infobiotics.dashboard.plugins.file_editors.editors.python_module_editor_handler
    import infobiotics.dashboard.plugins.file_editors.editors.abstract_file_editor
    import infobiotics.dashboard.plugins.file_editors.editors.python_module_editor
    import infobiotics.dashboard.plugins.file_editors.action_set
    import infobiotics.dashboard.plugins.text_editor.api
    import infobiotics.dashboard.plugins.text_editor.actions
    import infobiotics.dashboard.plugins.text_editor.text_editor_plugin
    import infobiotics.dashboard.plugins.text_editor.editor.text_editor_handler
    import infobiotics.dashboard.plugins.text_editor.editor.text_editor
    import infobiotics.dashboard.plugins.text_editor.text_editor_action_set
    import infobiotics.dashboard.plugins.mcss.ui_plugin
    import infobiotics.dashboard.plugins.mcss.actions
    import infobiotics.dashboard.plugins.mcss.action_set
    import infobiotics.dashboard.plugins.poptimizer.ui_plugin
    import infobiotics.dashboard.plugins.poptimizer.actions
    import infobiotics.dashboard.plugins.poptimizer.action_set
    import infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment_progress_handler
    import infobiotics.dashboard.poptimizer.api
    import infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment_handler
    import infobiotics.dashboard.poptimizer.poptimizer_dashboard_experiment
    import infobiotics.__version__
    import infobiotics.thirdparty.which
    import infobiotics.thirdparty.winpexpect.pexpect
    import infobiotics.thirdparty.winpexpect.winpexpect
    import infobiotics.mcss.mcss_experiment
    import infobiotics.mcss.mcss_params
    import infobiotics.mcss.results.mcss_results.mcss_results_editors
    import infobiotics.mcss.results.mcss_results.mcss_results_plots
    import infobiotics.mcss.results.mcss_results.mcss_results_views
    import infobiotics.mcss.results.mcss_results.mcss_results_handler
    import infobiotics.mcss.results.mcss_results.mcss_results_actions
    import infobiotics.mcss.results.mcss_results.mcss_results
    import infobiotics.mcss.results.mcss_results.mcss_results_groups
    import infobiotics.mcss.results.ideas
    import infobiotics.mcss.results.mcss_results_attributes
    import infobiotics.mcss.api
    import infobiotics.mcss.mcss_experiment_progress_handler
    import infobiotics.mcss.mcss_params_group
    import infobiotics.mcss.mcss_preferences
    import infobiotics.mcss.mcss_experiment_handler
    import infobiotics.mcss.mcss_params_handler
    import infobiotics.plugins.dashboard.default_action_set
    import infobiotics.plugins.dashboard.generic_actions
    import infobiotics.plugins.dashboard.plugin
    import infobiotics.plugins.dashboard.actions.open_action
    import infobiotics.plugins.dashboard.actions.close_all
    import infobiotics.plugins.dashboard.actions.save_as_action
    import infobiotics.plugins.dashboard.actions.example_action
    import infobiotics.plugins.dashboard.actions.close_action
    import infobiotics.plugins.dashboard.actions.python_module_action
    import infobiotics.plugins.dashboard.actions.open_python_module_action
    import infobiotics.plugins.dashboard.actions.new_window_action
    import infobiotics.plugins.dashboard.actions.untitled_text_file_action
    import infobiotics.plugins.dashboard.actions.about_action
    import infobiotics.plugins.dashboard.actions.open_text_file_action
    import infobiotics.plugins.dashboard.actions.save_action
    import infobiotics.plugins.dashboard.actions.exit_action
    import infobiotics.plugins.dashboard.actions.new_editor_action
    import infobiotics.plugins.dashboard.application
    import infobiotics.plugins.dashboard.editors.code_file_editor
    import infobiotics.plugins.dashboard.editors.api
    import infobiotics.plugins.dashboard.editors.text_file_editor
    import infobiotics.plugins.dashboard.editors.abstract_file_editor
    import infobiotics.plugins.dashboard.editors.python_module_editor
    import infobiotics.plugins.dashboard.generic_action_set
    import infobiotics.plugins.dashboard.core_action_set
    import infobiotics.poptimizer.poptimizer_experiment_progress_handler
    import infobiotics.poptimizer.api
    import infobiotics.poptimizer.poptimizer_experiment_handler
    import infobiotics.poptimizer.poptimizer_params_handler
    import infobiotics.poptimizer.poptimizer_experiment
    import infobiotics.poptimizer.poptimizer_params_group
    import infobiotics.poptimizer.poptimizer_results
    import infobiotics.poptimizer.poptimizer_preferences
    import infobiotics.poptimizer.poptimizer_params


# see below for setup.py INCLUDES

'''
Explicit imports for modules and packages that not automatically picked up by
modulefinder when running py2app and py2exe, in particular this includes 
Enthought's TraitsUI backend modules that are dynamically loaded.
'''

#if False: #TODO?

import sip
import PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qsci
from PyQt4 import QtNetwork

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


## explicitly include hard-to-find modules for py2app and py2exe
#INCLUDES = [
#    'sip',
#    'PyQt4',
#    'PyQt4.QtCore',
#    'PyQt4.QtGui',
#    'PyQt4.Qsci',
#    'PyQt4.QtNetwork',
#    'enthought.traits.ui.qt4',
#    'enthought.pyface.ui.qt4.action.action_item',
#    'enthought.pyface.ui.qt4.action.menu_manager',
#    'enthought.pyface.ui.qt4.action.menu_bar_manager',
#    'enthought.pyface.ui.qt4.action.status_bar_manager',
#    'enthought.pyface.ui.qt4.action.tool_bar_manager',
#    'enthought.tvtk.vtk_module',
#    'enthought.tvtk.pyface.ui.qt4.init',
#    'enthought.tvtk.pyface.ui.qt4',
#    'enthought.tvtk.pyface.ui.qt4.scene_editor',
#    'enthought.pyface.ui.qt4.about_dialog',
#    'enthought.pyface.ui.qt4.application_window',
#    'enthought.pyface.ui.qt4.clipboard',
#    'enthought.pyface.ui.qt4.confirmation_dialog',
#    'enthought.pyface.ui.qt4.dialog',
#    'enthought.pyface.ui.qt4.directory_dialog',
#    'enthought.pyface.ui.qt4.file_dialog',
#    'enthought.pyface.ui.qt4.gui',
#    'enthought.pyface.ui.qt4.heading_text',
#    'enthought.pyface.ui.qt4.image_cache',
#    'enthought.pyface.ui.qt4.image_resource',
#    'enthought.pyface.ui.qt4.init',
#    'enthought.pyface.ui.qt4.message_dialog',
#    'enthought.pyface.ui.qt4.progress_dialog',
#    'enthought.pyface.ui.qt4.python_editor',
#    'enthought.pyface.ui.qt4.python_shell',
#    'enthought.pyface.ui.qt4.resource_manager',
#    'enthought.pyface.ui.qt4.splash_screen',
#    'enthought.pyface.ui.qt4.split_widget',
#    'enthought.pyface.ui.qt4.system_metrics',
#    'enthought.pyface.ui.qt4.widget',
#    'enthought.pyface.ui.qt4.window',
#    'enthought.pyface.ui.qt4.workbench.editor',
#    'enthought.pyface.ui.qt4.workbench.split_tab_widget',
#    'enthought.pyface.ui.qt4.workbench.view',
#    'enthought.pyface.ui.qt4.workbench.workbench_window_layout',
#    'enthought.envisage.ui.workbench.action.api',
#    'enthought.plugins.ipython_shell.actions',
#    'enthought.plugins.ipython_shell.actions.ipython_shell_actions',
#    'enthought.plugins.refresh_code.actions',
#    'enthought.plugins.remote_editor.actions',
#    'enthought.plugins.text_editor.actions',
#    'enthought.tvtk.plugins.scene.ui.actions',
#    #TODO see py2exe_includes.py at http://markmail.org/thread/qkdwu7gbwrmop6so
#    'numpy',
#    'matplotlib',
#    'vtk',
#    'encodings',
#    'tables',
##    'pywintypes',
#]

#TODO from uniq-list (py2app 0.0.6 vs 0.0.7)
import infobiotics.api
import infobiotics.common.__init__
import infobiotics.common.api
import infobiotics.common.experiment
import infobiotics.common.experiment_handler
import infobiotics.common.experiment_progress_handler
import infobiotics.common.params
import infobiotics.common.params_handler
import infobiotics.common.params_preferences
import infobiotics.common.views
import infobiotics.commons.__init__
import infobiotics.commons.api
import infobiotics.commons.colours
import infobiotics.commons.dicts
import infobiotics.commons.files
import infobiotics.commons.lists
import infobiotics.commons.md5sum
import infobiotics.commons.qt4
import infobiotics.commons.sequences
import infobiotics.commons.strings
import infobiotics.commons.traits.__init__
import infobiotics.commons.traits.api
import infobiotics.commons.traits.float_greater_than_zero
import infobiotics.commons.traits.float_with_minimum
import infobiotics.commons.traits.int_greater_than_zero
import infobiotics.commons.traits.long_greater_than_zero
import infobiotics.commons.traits.relative_directory
import infobiotics.commons.traits.relative_file
import infobiotics.commons.traits.ui.__init__
import infobiotics.commons.traits.ui.api
import infobiotics.commons.traits.ui.fixed_file_dialog
import infobiotics.commons.traits.ui.helpful_controller
import infobiotics.commons.traits.ui.qt4.__init__
import infobiotics.commons.traits.ui.qt4.cancellable_progress_editor
import infobiotics.commons.traits.ui.qt4.relative_directory_editor
import infobiotics.commons.traits.ui.qt4.relative_file_editor
import infobiotics.commons.unified_logging
import infobiotics.commons.webbrowsing
import infobiotics.dashboard.api
import infobiotics.dashboard.mcss.__init__
import infobiotics.dashboard.mcss.api
import infobiotics.dashboard.mcss.mcss_dashboard_experiment
import infobiotics.dashboard.mcss.mcss_dashboard_experiment_handler
import infobiotics.dashboard.mcss.mcss_dashboard_experiment_progress_handler
import infobiotics.dashboard.plugins.core.__init__
import infobiotics.dashboard.plugins.core.action_set
import infobiotics.dashboard.plugins.core.preferences_page
import infobiotics.dashboard.plugins.core.ui_plugin
import infobiotics.dashboard.plugins.mcss.actions
import infobiotics.dashboard.plugins.pmodelchecker.action_set
import infobiotics.dashboard.plugins.pmodelchecker.actions
import infobiotics.dashboard.plugins.pmodelchecker.pmodelchecker_action_set
import infobiotics.dashboard.plugins.poptimizer.__init__
import infobiotics.dashboard.plugins.poptimizer.action_set
import infobiotics.dashboard.plugins.poptimizer.actions
import infobiotics.dashboard.plugins.poptimizer.ui_plugin
import infobiotics.dashboard.plugins.simulator_results.FromToDoubleSpinBox
import infobiotics.dashboard.plugins.simulator_results.PlotsListWidget
import infobiotics.dashboard.plugins.simulator_results.actions
import infobiotics.dashboard.plugins.simulator_results.editor
import infobiotics.dashboard.plugins.simulator_results.icons_rc
import infobiotics.dashboard.plugins.simulator_results.main
import infobiotics.dashboard.plugins.simulator_results.simulator_results
import infobiotics.dashboard.plugins.simulator_results.ui_player_control_widget
import infobiotics.dashboard.plugins.simulator_results.ui_plots_preview_dialog
import infobiotics.dashboard.plugins.simulator_results.ui_simulation_results_dialog
import infobiotics.mcss.__init__
import infobiotics.mcss.api
import infobiotics.mcss.mcss_experiment
import infobiotics.mcss.mcss_experiment_handler
import infobiotics.mcss.mcss_experiment_progress_handler
import infobiotics.mcss.mcss_params
import infobiotics.mcss.mcss_params_group
import infobiotics.mcss.mcss_params_handler
import infobiotics.mcss.mcss_preferences
import infobiotics.pmodelchecker.__init__
import infobiotics.pmodelchecker.api
import infobiotics.pmodelchecker.mc2.__init__
import infobiotics.pmodelchecker.mc2.api
import infobiotics.pmodelchecker.mc2.mc2_experiment
import infobiotics.pmodelchecker.mc2.mc2_experiment_handler
import infobiotics.pmodelchecker.mc2.mc2_experiment_progress_handler
import infobiotics.pmodelchecker.mc2.mc2_mcss_experiment
import infobiotics.pmodelchecker.mc2.mc2_mcss_experiment_group
import infobiotics.pmodelchecker.mc2.mc2_params
import infobiotics.pmodelchecker.mc2.mc2_params_group
import infobiotics.pmodelchecker.mc2.mc2_params_handler
import infobiotics.pmodelchecker.model_parameters
import infobiotics.pmodelchecker.pmodelchecker_experiment
import infobiotics.pmodelchecker.pmodelchecker_params
import infobiotics.pmodelchecker.pmodelchecker_params_handler
import infobiotics.pmodelchecker.pmodelchecker_preferences
import infobiotics.pmodelchecker.prism.__init__
import infobiotics.pmodelchecker.prism.api
import infobiotics.pmodelchecker.prism.prism_experiment
import infobiotics.pmodelchecker.prism.prism_experiment_handler
import infobiotics.pmodelchecker.prism.prism_experiment_progress_handler
import infobiotics.pmodelchecker.prism.prism_params
import infobiotics.pmodelchecker.prism.prism_params_group
import infobiotics.pmodelchecker.prism.prism_params_handler
import infobiotics.pmodelchecker.temporal_formulas
import infobiotics.thirdparty.__init__
import infobiotics.thirdparty.pexpect
import infobiotics.thirdparty.which
import infobiotics.thirdparty.winpexpect

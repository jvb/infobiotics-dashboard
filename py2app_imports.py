'''
Explicit imports for modules and packages that not automatically picked up by
py2app, in particular enthought GUI backend modules that are dynamically loaded.
'''

import sip
from PyQt4 import *
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

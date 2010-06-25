# see below for setup.py INCLUDES

'''
Explicit imports for modules and packages that not automatically picked up by
modulefinder when running py2app and py2exe, in particular this includes 
Enthought's TraitsUI backend modules that are dynamically loaded.
'''

import sip
import PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qsci
#from PyQt4 import QtNetwork

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

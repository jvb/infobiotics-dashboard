import os
from PyQt4 import QtGui
from ...api import Str
from .file_editor2 import SimpleEditor as SimpleFileEditor, FileEditor

class SimpleEditor(SimpleFileEditor):
    
    def _create_file_dialog ( self ):
        """ Creates the correct type of file dialog.
        """
        dlg = super(SimpleEditor, self)._create_file_dialog()
        dlg.setFileMode(QtGui.QFileDialog.Directory)
        return dlg

class DirectoryEditor(FileEditor): # EditorFactory
    pass
    
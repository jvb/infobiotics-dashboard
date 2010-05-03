from relative_file_editor import SimpleEditor as SimpleRelativeFileEditor, RelativeFileEditor
from PyQt4 import QtGui

class SimpleEditor(SimpleRelativeFileEditor):
    
    def _create_file_dialog(self):
        ''' Creates the correct type of file dialog. '''
        dlg = super(SimpleEditor, self)._create_file_dialog()
        dlg.setFileMode(QtGui.QFileDialog.Directory)
        return dlg

class RelativeDirectoryEditor(RelativeFileEditor): # EditorFactory
    
    def _get_simple_editor_class(self):
        return SimpleEditor

    def _get_custom_editor_class(self):
        return SimpleEditor
    
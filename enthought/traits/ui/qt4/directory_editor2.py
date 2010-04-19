from PyQt4 import QtGui
from ...api import Str
from enthought.traits.directory import Directory 
from .file_editor2 import _FileEditor, FileEditor

class _DirectoryEditor(_FileEditor):
    """ Simple style of editor for directories, which displays a text field
        and a **Browse** button that opens a directory-selection dialog box.
    """
    
#    def _directory_changed(self):
#        print '_DirectoryEditor._directory_changed(self):', self.directory
#    def _directory_name_changed(self):
#        print '_DirectoryEditor._directory_name_changed(self):', self.directory_name
    
    def _create_file_dialog ( self ):
        """ Creates the correct type of file dialog.
        """
        dlg = super(_DirectoryEditor, self)._create_file_dialog()
        dlg.setFileMode(QtGui.QFileDialog.Directory)
        return dlg
        

class DirectoryEditor(FileEditor): # EditorFactory
    
    directory = Directory(exists=True)
    directory_name = Str

    def _directory_default(self):
        import os
        return os.getcwd()

#    def _directory_changed(self):
#        print 'DirectoryEditor._directory_changed(self):', self.directory
#    def _directory_name_changed(self):
#        print 'DirectoryEditor._directory_name_changed(self):', self.directory_name
    
    def _get_simple_editor_class(self):
        return _DirectoryEditor
    def _get_custom_editor_class(self):
        return _DirectoryEditor
    
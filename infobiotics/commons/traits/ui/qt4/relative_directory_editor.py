from infobiotics.commons.traits.ui.qt4.relative_file_editor import SimpleEditor as SimpleRelativeFileEditor
from infobiotics.commons.traits.ui.qt4.relative_file_editor import RelativeFileEditor 
from PyQt4 import QtGui
from PyQt4.QtCore import QDir

class SimpleEditor(SimpleRelativeFileEditor):
    
    def _create_file_dialog(self):
        ''' Creates the correct type of file dialog. '''
        dlg = QtGui.QFileDialog(self.control.parentWidget(), self.name, self.directory)
        dlg.setFileMode(QtGui.QFileDialog.Directory)
#        dlg.setOption(QtGui.QFileDialog.ShowDirsOnly)
        dlg.setFilter(QDir.Dirs)
        if len(self.factory.filter) > 0:
            dlg.setNameFilters(self.factory.filter)
        return dlg

    def show_file_dialog(self):
        ''' Displays the pop-up file dialog. '''
        # We don't used the canned functions because we don't know how the
        # file name is to be used (ie. an existing one to be opened or a new
        # one to be created).
        dlg = self._create_file_dialog()
        if dlg.exec_() == QtGui.QDialog.Accepted:
            files = dlg.selectedFiles()
            if len(files) > 0:
                file_name = unicode(files[0])
                if self.factory.truncate_ext:
                    file_name = os.path.splitext(file_name)[0]
                if not self.factory.absolute:
                    file_name = os.path.relpath(file_name, self.directory) 
                self.update_editor(file_name)
                self.update_object()


class RelativeDirectoryEditor(RelativeFileEditor): # EditorFactory
    
    def _get_simple_editor_class(self):
        return SimpleEditor

    def _get_readonly_editor_class(self):
        return SimpleTextEditor
    
    def _get_custom_editor_class(self):
        return SimpleEditor
    
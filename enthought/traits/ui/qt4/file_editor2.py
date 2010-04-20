'''
Adapted from qt4/extras/bounds_editor.py and qt4/file_editor.py 
'''

import os.path
from PyQt4 import QtCore, QtGui
from ...api import (TraitError, Str, Directory)
from ..api import FileEditor
from .text_editor import SimpleEditor as SimpleTextEditor

class _FileEditor(SimpleTextEditor):

    directory = Directory(exists=True)
    directory_name = Str

#    def _directory_changed(self):
#        print '_FileEditor._directory_changed(self):', self.directory
#    def _directory_name_changed(self):
#        print '_FileEditor._directory_name_changed(self):', self.directory_name

    def init(self, parent):
        
        factory = self.factory # FileEditor (below)
        if not factory.directory_name:
            self.directory = factory.directory
        else:
            self.sync_value(factory.directory_name, 'directory', 'both')#TODO just 'from'?

        self.control = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(self.control)
        layout.setMargin(0)

        self._file_name = control = QtGui.QLineEdit()
        layout.addWidget(control)

        if self.factory.auto_set:
            signal = QtCore.SIGNAL('textEdited(QString)')
        else:
            # Assume enter_set is set, or else the value will never get updated.
            signal = QtCore.SIGNAL('editingFinished()')
        QtCore.QObject.connect(control, signal, self.update_object)

        button = QtGui.QPushButton("Browse...")
        layout.addWidget(button)

        QtCore.QObject.connect(button, QtCore.SIGNAL('clicked()'), 
                               self.show_file_dialog)

        self.set_tooltip(control)
        
        self.set_value(self.value)


    def update_object(self):
        """ Handles the user changing the contents of the edit control.
        """
        self._update(unicode(self._file_name.text()))


    def update_editor ( self, value=None):
        """ Updates the editor when the object trait changes externally to the 
            editor.
        """
        if value is not None:
            self._file_name.setText(value)
        else: 
            self._file_name.setText(self.str_value)


    def show_file_dialog(self):
        """ Displays the pop-up file dialog.
        """
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

                self.set_value(file_name)#self.value = file_name
                self.update_editor(file_name)


    def get_error_control ( self ):
        """ Returns the editor's control for indicating error status.
        """
        return self._file_name


    def _create_file_dialog ( self ):
        """ Creates the correct type of file dialog.
        """
        dlg = QtGui.QFileDialog(self.control.parentWidget())
        dlg.setDirectory(self.directory)
        dlg.selectFile(self._file_name.text())

        if len(self.factory.filter) > 0:
            dlg.setFilters(self.factory.filter)

        return dlg

    def _update ( self, file_name ):
        """ Updates the editor value with a specified file name.
        """
        try:
            if self.factory.truncate_ext:
                file_name = os.path.splitext( file_name )[0]

            self.set_value(file_name)#self.value = file_name
        except TraitError, excp:
            pass

    # Fixes non-removal of error state
    def set_value(self, value):
        try:
            
            if not os.path.isabs(value):
                if not os.path.isabs(self.directory):
                    value = os.path.join(os.path.getcwd(), self.directory, value)
                else:
                    value = os.path.join(self.directory, value)

            self.value = value

            if self._error is not None:
                self._error = None
                self.ui.errors -= 1

            self.set_error_state(False)
                
        except TraitError, excp:
            pass


class FileEditor(FileEditor): # EditorFactory
    
    directory = Directory(exists=True)
    directory_name = Str

    def _directory_default(self):
        import os
        return os.getcwd()

#    def _directory_changed(self):
#        print 'FileEditor._directory_changed(self):', self.directory
#    def _directory_name_changed(self):
#        print 'FileEditor._directory_name_changed(self):', self.directory_name
    
    def _get_simple_editor_class(self):
        return _FileEditor
    def _get_custom_editor_class(self):
        return _FileEditor
    
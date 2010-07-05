'''
Adapted from qt4/extras/bounds_editor.py, qt4/file_editor.py, and qt4/html_editor.py
'''

from enthought.traits.ui.qt4.text_editor import SimpleEditor as SimpleTextEditor
from enthought.traits.ui.api import FileEditor
from enthought.traits.api import Str, Bool, TraitError, on_trait_change
from infobiotics.commons.traits.relative_directory import RelativeDirectory
from infobiotics.commons.strings import wrap
import os
from PyQt4 import QtCore, QtGui

class SimpleEditor(SimpleTextEditor):

    directory = RelativeDirectory(exists=True)
    exists = Bool(False)
    
    def init(self, parent):
        factory = self.factory # RelativeFileEditor below
        self.directory = factory.directory
        self.sync_value(factory.directory_name, 'directory', 'from')
        self.sync_value(factory.exists_name, 'exists', 'from')
            
        # same as file_editor.SimpleEditor ---
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

        self.set_tooltip(control) # != self.control
        # end of similarity ---
        
        # ensure invalid is set appropriately for hard-coded/default value ---
        if self.value is not None:
#            self.update_object()
            print 'value =', self.value
            self.update_editor(self.value)

    @on_trait_change('exists, directory')
    def update_object(self):
        ''' Handles the user changing the contents of the edit control. '''
        if self.control is not None:
            self._update(unicode(self._file_name.text()))

    def update_editor(self, value=None):
        ''' Updates the editor when the object trait changes externally to the editor. ''' 
        if value is not None:
            self._file_name.setText(value) # triggers update_object
        else: 
            self._file_name.setText(self.str_value) # triggers update_object
        self.update_object() 
        # needed to refresh invalid state when a valid value is set while the 
        # editor is in an invalid state

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

    def get_error_control(self):
        ''' Returns the editor's control for indicating error status. '''
        return self._file_name

    def _create_file_dialog(self):
        ''' Creates the correct type of file dialog. '''
        dlg = QtGui.QFileDialog(self.control.parentWidget(), self.name, self.directory)
        if self.exists: 
            dlg.setFileMode(QtGui.QFileDialog.ExistingFile)
        if len(self.factory.filter) > 0:
            dlg.setNameFilters(self.factory.filter)
        
        dlg.selectFile(self._file_name.text())
        
        return dlg

    def _update(self, file_name):
        ''' Updates the editor value with a specified file name. '''
        try:
            if self.factory.truncate_ext:
                file_name = os.path.splitext(file_name)[0]
            self.value = file_name
            if self._error is not None:
                self._error = None
                self.ui.errors -= 1
            self.set_error_state(False)
            if self.description == '' and self.object.base_trait(self.name).desc is None:
                self._file_name.setToolTip('') # restore '' over excp
            else:
                self.set_tooltip(self._file_name) # restore desc over excp
        except TraitError, excp:
            self._file_name.setToolTip(wrap(unicode(excp),80))
            self.error(excp)

class RelativeFileEditor(FileEditor): # EditorFactory
    
    absolute = Bool(False)
    directory = RelativeDirectory(exists=True)
    directory_name = Str
    exists = Bool(False)
    exists_name = Str

    def _directory_default(self):
        return os.getcwd()
    
    def _get_simple_editor_class(self):
        return SimpleEditor

    def _get_readonly_editor_class(self):
        return SimpleTextEditor

    def _get_custom_editor_class(self):
        return SimpleEditor
    
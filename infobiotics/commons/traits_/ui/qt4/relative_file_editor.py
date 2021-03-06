'''
Adapted from qt4/extras/bounds_editor.py, qt4/file_editor.py, and qt4/html_editor.py
'''

from traitsui.qt4.text_editor import SimpleEditor as SimpleTextEditor, ReadonlyEditor
from traitsui.api import FileEditor
from traits.api import Str, Bool, TraitError, on_trait_change
#from infobiotics.commons.strings import wrap
import os
from PyQt4 import QtCore, QtGui
import textwrap

class SimpleEditor(SimpleTextEditor):

    directory = Str
    exists = Bool(False)
    empty_ok = Bool(False)
    
    def init(self, parent):
        factory = self.factory # RelativeFileEditor below
        self.directory = factory.directory
        self.sync_value(factory.directory_name, 'directory', 'from')
        self.sync_value(factory.exists_name, 'exists', 'from')
        self.sync_value(factory.empty_ok_name, 'empty_ok', 'from')
            
        # same as traitsui.qt4.file_editor.SimpleEditor ---
        self.control = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(self.control)
        layout.setMargin(0)

        self._file_name = control = QtGui.QLineEdit()
        layout.addWidget(control)

        if self.factory.auto_set:
            signal = QtCore.SIGNAL('textEdited(QString)') # Unlike textChanged(), this signal is not emitted when the text is changed programmatically, for example, by calling setText().
        else:
            # Assume enter_set is set, or else the value will never get updated.
            signal = QtCore.SIGNAL('editingFinished()') # This signal is emitted when the Return or Enter key is pressed or the line edit loses focus.
        QtCore.QObject.connect(control, signal, self.update_object)

        button = QtGui.QPushButton("Browse...")
        layout.addWidget(button)

        QtCore.QObject.connect(button, QtCore.SIGNAL('clicked()'),
                               self.show_file_dialog)

        self.set_tooltip(control) # != self.control
        # end of similarity ---
        
#        # ensure invalid is set appropriately for hard-coded/default value ---
#        if self.value is not None:
#            self.update_editor(self.value) # which then calls self.update_object, which in turn calls self._update

    @on_trait_change('directory, exists, empty_ok')
    def update_object(self):
        ''' Handles the user changing the contents of the edit control. '''
        if self.control is not None:
            self._update(unicode(self._file_name.text()))
            
    def update_editor(self, value=None):
        ''' Updates the editor when the object trait changes externally to the editor. ''' 
        if value is not None:
            self._file_name.setText(value)
        else: 
            self._file_name.setText(self.value)

        self.update_object()
        # needed to refresh invalid state when a valid value is set while the 
        # editor is in an invalid state

    def show_file_dialog(self):
        ''' Displays the pop - up file dialog. '''
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
        width = 80
        try:
            if self.factory.truncate_ext:
                file_name = os.path.splitext(file_name)[0]
            self.value = file_name
            if self._error is not None:
                self._error = None
                self.ui.errors -= 1
            self.set_error_state(False)
            if not self.set_tooltip(self._file_name): # restore desc over excp
                self._file_name.setToolTip(textwrap.fill(self.object.base_trait(self.name).full_info(self.object, self.name, self.value), width=width)) # set tooltip over excp using traits info
        except TraitError, excp:
            self._file_name.setToolTip(textwrap.fill(unicode(excp), width=width)) # fix tooltip line lengths
            self.error(excp)


class RelativeFileEditor(FileEditor): # EditorFactory
    
    absolute = Bool(False)
    directory = Str
    directory_name = Str
    exists = Bool(False)
    exists_name = Str
    empty_ok = Bool(False)
    empty_ok_name = Str
    
    def _get_simple_editor_class(self):
        return SimpleEditor

    def _get_readonly_editor_class(self):
        return ReadonlyEditor

    def _get_custom_editor_class(self):
        return SimpleEditor
    

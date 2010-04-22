if __name__ == '__main__': #TODO
    execfile('../../file.py')
    exit()

'''
Adapted from qt4/extras/bounds_editor.py and qt4/file_editor.py 
'''

import os
from PyQt4 import QtCore, QtGui
from ...api import TraitError, Str, Property
from ..api import FileEditor
from .text_editor import SimpleEditor as SimpleTextEditor
from common.strings import wrap
from enthought.traits.directory import Directory

class SimpleEditor(SimpleTextEditor):

    directory = Directory(exists=True)
    def _directory_changed(self):
        print 'SimpleEditor._directory_changed(self):', self.directory

    directory_name = Str
#    directory_name = Property(desc='...overrides directory trait', handler='_directory_name_changed')
#    def _get_directory_name(self):
#        return self._directory_name
#    def _set_directory_name(self, directory_name):
#        self._directory_name = self.factory.named_value(directory_name, self.ui)
    def _directory_name_changed(self, old, new):
        print "SimpleEditor._directory_name_changed(self, old='%s', new='%s')" % (old, new)
##        self.sync_value(new, 'directory', 'from')

    def init(self, parent):
        # initialise traits from factory
        factory = self.factory # FileEditor (below)
        if factory.directory_name:
            factory.sync_trait('directory_name', self)
            self.sync_value(factory.directory_name, 'directory', 'from')
        else:
            factory.sync_trait('directory', self)
#            self.sync_value(factory.directory, 'directory', 'from')
            
        # file_editor.SimpleEditor ---
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
        # end of file_editor.SimpleEditor ---
        
        # ensure invalid is set appropriately for hard-coded/default value ---
        if self.value is not None:
            self.set_value(self.value)
#        else:
#            self.set_value('hello')

    def update_object(self):
        """ Handles the user changing the contents of the edit control.
        """
        self._update(unicode(self._file_name.text()))

    def update_editor (self, value=None):
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
        dlg = QtGui.QFileDialog(self.control.parentWidget(), self.name, self.directory)
        if self.object.base_trait(self.name).handler.exists: 
            dlg.setFileMode(QtGui.QFileDialog.ExistingFile)
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

    def set_value(self, value):
        ''' Fixes non-removal of invalid state. '''
        try:
            self.value = value

            # added
            if self._error is not None:
                self._error = None
                self.ui.errors -= 1

            self.set_error_state(False)

            if self.description == '' and self.object.base_trait( self.name ).desc is None:
                self._file_name.setToolTip('') # restore '' over excp
            else:
                self.set_tooltip(self._file_name) # restore desc over excp
                
        except TraitError, excp:
            self._file_name.setToolTip(wrap(unicode(excp),80)) #TODO plus desc?


class FileEditor(FileEditor): # EditorFactory
    
    directory = Directory(exists=True, desc='overrides File(directory=...)')
    def _directory_default(self):
        return os.getcwd()
    def _directory_changed(self, old, new):
        print 'FileEditor._directory_changed(self, old, new):', old, new

    directory_name = Str(desc='...overrides directory trait')
    def _directory_name_changed(self):
        print 'FileEditor._directory_name_changed(self):', self.directory_name
    
    def _get_simple_editor_class(self):
        return SimpleEditor
    def _get_custom_editor_class(self):
        return SimpleEditor
    
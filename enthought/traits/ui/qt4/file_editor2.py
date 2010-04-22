if __name__ == '__main__': #TODO
    execfile('../../file2.py')
    exit()

'''
Adapted from qt4/extras/bounds_editor.py and qt4/file_editor.py 
'''

import os
from PyQt4 import QtCore, QtGui
from ...api import (TraitError, Str, Directory)
from ..api import FileEditor
from .text_editor import SimpleEditor as SimpleTextEditor

class SimpleEditor(SimpleTextEditor):

    directory = Directory(exists=True)
    directory_name = Str
    def _directory_changed(self):
        print 'SimpleEditor._directory_changed(self):', self.directory
    def _directory_name_changed(self, old, new):
        print "SimpleEditor._directory_name_changed(self, old='%s', new='%s')" % (old, new)
#        self.sync_value(new, 'directory', 'from')
        
    def init(self, parent):
        # initialise traits from factory
        factory = self.factory # FileEditor (below)
        if factory.directory_name:
            print '1'
#            factory.sync_trait('directory_name', self)
#            self.sync_value(factory.directory_name, 'directory', 'from')
            self.sync_value(factory.directory_name, 'directory_name', 'from')
        else:
            print '2'
#            factory.sync_trait('directory', self)
#            factory.sync_trait('directory_name', self, remove=True)
            self.sync_value(factory.directory, 'directory', 'from')
        print self._get_sync_trait_info()
        print factory._get_sync_trait_info()
            
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
        else:
            self.set_value('hello')


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

#    def resolve_value(self, value): #TODO see todo below
##        if not os.path.isabs(value):
##            if not os.path.isabs(self.directory):
##                abspath = os.path.join(os.getcwd(), self.directory, value)
##            else:
##                abspath = os.path.join(self.directory, value)
##            return os.path.relpath(value, abspath)
#        return value
    
    def set_value(self, value):
        ''' Fixes non-removal of invalid state. '''
        try:
#            value = self.resolve_value(value) # is done at the trait-level #TODO might need to do it here too if directory/directory_name attribute of trait is not set but they are set in the editor...   
            self.value = value

            # added
            if self._error is not None:
                self._error = None
                self.ui.errors -= 1

            self.set_error_state(False)
                
            self.set_tooltip(self._file_name) # restore desc over excp
                
        except TraitError, excp:
            self._file_name.setToolTip(unicode(excp)) # #TODO plus desc?


    def sync_value ( self, user_name, editor_name, mode = 'both',
                           is_list = False, remove=False ):
        """ Sets or unsets synchronization between an editor trait and a user
            object trait.
        """
        if user_name != '':
            key = '%s:%s' % ( user_name, editor_name )

            if self._no_trait_update is None:
                self._no_trait_update = {}

            user_ref = 'user_object'
            col      = user_name.find( '.' )
            if col < 0:
                user_object = self.context_object
                xuser_name  = user_name
            else:
                user_object = self.ui.context[ user_name[ : col ] ]
                user_name   = xuser_name = user_name[ col + 1: ]
                col         = user_name.rfind( '.' )
                if col >= 0:
                    user_ref += ('.' + user_name[ : col ])
                    user_name = user_name[ col + 1: ]

            user_value = compile( '%s.%s' % ( user_ref, user_name ),
                                  '<string>', 'eval' )
            user_ref   = compile( user_ref, '<string>', 'eval' )

            if mode in ( 'from', 'both' ):

                def user_trait_modified ( new ):
                    # Need this to include 'user_object' in closure:
                    user_object
                    if key not in self._no_trait_update:
                        self._no_trait_update[ key ] = None
                        try:
                            setattr( self, editor_name, new )
                        except:
                            pass
                        del self._no_trait_update[ key ]

                user_object.on_trait_change( user_trait_modified, xuser_name, remove=remove )

                if self._user_to is None:
                    self._user_to = []
                self._user_to.append( ( user_object, xuser_name,
                                        user_trait_modified ) )

                if is_list:

                    def user_list_modified ( event ):
                        if isinstance( event, TraitListEvent ):
                            if key not in self._no_trait_update:
                                self._no_trait_update[ key ] = None
                                n = event.index
                                try:
                                    getattr( self, editor_name )[
                                        n: n + len(event.removed)] = event.added
                                except:
                                    pass
                                del self._no_trait_update[ key ]

                    user_object.on_trait_change( user_list_modified,
                                    xuser_name + '_items', remove=remove )
                    self._user_to.append( ( user_object, xuser_name + '_items',
                                            user_list_modified ) )

                try:
                    setattr( self, editor_name, eval( user_value ) )
                except:
                    pass

            if mode in ( 'to', 'both' ):

                def editor_trait_modified ( new ):
                    # Need this to include 'user_object' in closure:
                    user_object
                    if key not in self._no_trait_update:
                        self._no_trait_update[ key ] = None
                        try:
                            setattr( eval( user_ref ), user_name, new )
                        except:
                            pass
                        del self._no_trait_update[ key ]

                self.on_trait_change( editor_trait_modified, editor_name )

                if self._user_from is None:
                    self._user_from = []
                self._user_from.append( ( editor_name, editor_trait_modified ) )

                if is_list:

                    def editor_list_modified ( event ):
                        # Need this to include 'user_object' in closure:
                        user_object
                        if key not in self._no_trait_update:
                            self._no_trait_update[ key ] = None
                            n = event.index
                            try:
                                eval( user_value )[ n:
                                    n + len( event.removed ) ] = event.added
                            except:
                                pass
                            del self._no_trait_update[ key ]

                    self.on_trait_change( editor_list_modified,
                             editor_name + '_items' )
                    self._user_from.append( ( editor_name + '_items',
                                              editor_list_modified ) )

                if mode == 'to':
                    try:
                        setattr( eval( user_ref ), user_name,
                                 getattr( self, editor_name ) )
                    except:
                        pass


class FileEditor(FileEditor): # EditorFactory
    
    directory = Directory(exists=True) #TODO copy changes in file2.py to directory2.py and use its Directory here
    def _directory_default(self):
        # handles editor=FileEditor()
        return os.getcwd()

    directory_name = Str(desc='...overrides directory trait')
    
    def _directory_changed(self):
        print 'FileEditor._directory_changed(self):', self.directory
    def _directory_name_changed(self):
        print 'FileEditor._directory_name_changed(self):', self.directory_name
    
    def _get_simple_editor_class(self):
        return SimpleEditor
    def _get_custom_editor_class(self):
        return SimpleEditor
    
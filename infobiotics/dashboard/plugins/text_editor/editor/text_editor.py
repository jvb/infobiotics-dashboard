import os.path
from enthought.pyface.workbench.api import TraitsUIEditor
from enthought.pyface.api import FileDialog, CANCEL
from enthought.traits.api import Code, Instance
from enthought.traits.ui.api import CodeEditor, Group, Item, View
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings
from enthought.traits.ui.menu import NoButtons
from text_editor_handler import TextEditorHandler

def _id_generator():
    ''' A generator that returns the next number for untitled files. '''
    i = 1
    while True:
        yield(i)
        i += 1

_id_generator = _id_generator()

class TextEditor(TraitsUIEditor):
    ''' A text editor. '''
    
    text = Code # the text being edited

    key_bindings = Instance(KeyBindings) # key bindings used by the editor

    def _key_bindings_default(self):
        key_bindings = KeyBindings(
            KeyBinding(
                binding1    = 'Ctrl-s',
                description = 'Save the file',
                method_name = 'save'),
            KeyBinding(
                binding1    = 'Ctrl-r',
                description = 'Run the file',
                method_name = 'run'),
        )
        return key_bindings
        
    def save(self):
        ''' Saves the text to disk, prompting if not yet saved. '''
        if len(self.obj.path) == 0:
            self.save_as()
        else:
            f = file(self.obj.path, 'w')
            f.write(self.text)
            f.close()
            self.dirty = False # We have just saved the file so we ain't dirty no more!

    def save_as(self):
        ''' Saves the text to disk after prompting for the file name. '''
        dialog = FileDialog(
            parent           = self.window.control,
            action           = 'save as',
            default_filename = self.name,
            wildcard         = FileDialog.WILDCARD_PY #TODO remove
        )
        if dialog.open() != CANCEL:
            
            # update this editor
            self.id   = dialog.path
            self.name = os.path.basename(dialog.path)
            
            self.obj.path = dialog.path # update obj (an enthought.io.api.File) 

            self.save() # save it now it has a path
    
    def run(self):
        ''' Runs the file as Python. '''
        
        self.save() # The file must be saved first! #TODO do the same with experiments 
        
        if os.path.splitext(self.obj.path)[1] not in ('.py','.pyw'):
            print 'Not a Python file!'
            return 
        
        # Execute the code.
        if len(self.obj.path) > 0:
            view = self.window.get_view_by_id(
                'enthought.plugins.python_shell_view'
            )
            if view is not None:
                view.execute_command(
                    'execfile(r"%s")' % self.obj.path, 
                    hidden=False
                )
    
    def select_line(self, lineno):
        ''' Selects the specified line. '''
        self.ui.info.text.selected_line = lineno
        
    def _obj_changed(self, new):
        if len(new.path) == 0: # the path will be the empty string if we are editing a file that has not yet been saved.
            self.id   = self._get_unique_id()
            self.name = self.id
        else:
            self.id   = new.path
            self.name = os.path.basename(new.path)

            f = file(new.path, 'r')
            self.text = f.read()
            f.close()
    
    def _get_unique_id(self, prefix='Untitled '):
        ''' Return a unique id for a new file. '''
        id = prefix + str(_id_generator.next())
        while self.window.get_editor_by_id(id) is not None:
            id = prefix + str(_id_generator.next())
        return id
        
    def _text_changed(self, trait_name, old, new):
        if self.traits_inited(): #TODO is 'traits_inited' from HasTraits? 
            self.dirty = True #TODO Could this be a better pattern for 'dirty'?
    
    def _dirty_changed(self, dirty):
        if len(self.obj.path) > 0:
            if dirty:
                self.name = os.path.basename(self.obj.path) + '*'
            else:
                self.name = os.path.basename(self.obj.path)

    def create_ui(self, parent):
        ''' Creates the traits UI that represents the editor. '''
        ui = self.edit_traits(
            parent=parent, 
            view=self._create_traits_ui_view(), 
            kind='subpanel',
        )
        return ui
    
    def _create_traits_ui_view(self):
        ''' Create the traits UI view used by the editor. '''
        return View(
            Group(
                Item(
                    'text', editor=CodeEditor(
                        key_bindings=self.key_bindings,
                    ),
                ),
                show_labels = False # D'oh! I was using show_label=False for every item.
            ),

            id        = 'text_editor',
            handler   = TextEditorHandler(), # necessary for KeyBindings to function 
            kind      = 'live',
            resizable = True,
            width     = 1.0,
            height    = 1.0,
            buttons   = NoButtons,
        )    

from enthought.traits.ui.api import Handler
from enthought.pyface.workbench.api import TraitsUIEditor
from enthought.traits.api import Any, List, Tuple, Str, Instance
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings
from enthought.traits.ui.api import Handler, Group, Item, View 
from enthought.traits.ui.menu import NoButtons
import os.path
from enthought.pyface.api import FileDialog, CANCEL

class FileEditorHandler(Handler):
    ''' Necessary for KeyBindings to function. '''
    def save(self, info):
        ''' Save the file to disk. '''
        info.object.save()

save_key_binding = KeyBinding( # a reusable key binding
    binding1    = 'Ctrl-s',
    description = 'Save the file',
    method_name = 'save')
 
class AbstractFileEditor(TraitsUIEditor):
    ''' An abstract file editor. '''
    
    content = Any # the contents of the file being edited

    wildcards = List(Tuple(Str,List(Str)), desc="e.g. [('Python files',['*.py','*.pyw'])], defaults to 'All files (*)'.")

    key_bindings = Instance(KeyBindings) # key bindings used by the editor
    def _key_bindings_default(self):
        return KeyBindings(
            save_key_binding, # using reusable key bindings
        )
    
    handler = Instance(Handler)
    def _handler_default(self):
        return FileEditorHandler()    

    group = Instance(Group) 
    def _group_default(self):
        return Group(
            Item('content', style='custom'),
            show_labels = False # D'oh! I was using show_label=False for every item.
        )
            
    def _create_traits_ui_view(self):
        ''' Overload this method to create the traits UI view used by the editor. '''
        return View(
            self.group,
            buttons      = NoButtons,
            width        = 1.0,
            height       = 1.0,
            resizable    = True,
            kind         = 'live',
            id           = self.id,
            key_bindings = self.key_bindings,
            handler      = self.handler, # necessary for KeyBindings to function
        ) 


    def save_(self, file):
        ''' Overload this method to implement saving the file. '''
        raise NotImplementedError
    
    def load_(self, file):
        ''' Overload this method to implement loading the file. '''
        raise NotImplementedError
    
    def save(self):
        ''' Saves the file to disk, prompting if not yet saved. '''
        if len(self.obj.path) == 0:
            self.save_as()
        else:
            f = file(self.obj.path, 'w')
            self.save_(f) # call overloadable method that actually does the saving
            f.close()
            self.dirty = False # We have just saved the file so we ain't dirty no more!
            
    def save_as(self):
        ''' Saves the file to disk after prompting for the file name. '''
        dialog = FileDialog(
            parent           = self.window.control,
            action           = 'save as',
            default_filename = self.name,
#            wildcard         = '\n'.join([FileDialog.create_wildcard(wildcard[0], ' '.join(wildcard[1])) for wildcard in self.wildcards]) if len(self.wildcards) > 0 else FileDialog.create_wildcard('All files', '*')
            wildcard         = '\n'.join([FileDialog.create_wildcard(wildcard[0], ', '.join(wildcard[1])) for wildcard in self.wildcards]) if len(self.wildcards) > 0 else FileDialog.create_wildcard('All files', '*') #TODO test or remove
        )
        if dialog.open() != CANCEL:
            
            # update this editor
            self.id   = dialog.path
            self.name = os.path.basename(dialog.path)
            
            self.obj.path = dialog.path # update obj (an enthought.io.api.File) 

            self.save() # save it now it has a path

    def _obj_changed(self, new):
        if len(new.path) == 0: # the path will be the empty string if we are editing a file that has not yet been saved.
            self.id   = self._get_unique_id()
            self.name = self.id
        else:
            self.id   = str(new.path)
            self.name = os.path.basename(new.path)

            f = file(new.path, 'r')
            self.load_(f) # call overloadable method that actually does the loading
            f.close()
            
    def _get_unique_id(self, prefix='Untitled '):
        ''' Return a unique id for a new file. '''
        id = prefix + str(_id_generator.next())
        while self.window.get_editor_by_id(id) is not None:
            id = prefix + str(_id_generator.next())
        return id
        
    def _content_changed(self, trait_name, old, new):
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

def _id_generator(): # used by AbstractFileEditor._get_unique_id above
    ''' A generator that returns the next number for untitled files. '''
    i = 1
    while True:
        yield(i)
        i += 1
_id_generator = _id_generator()

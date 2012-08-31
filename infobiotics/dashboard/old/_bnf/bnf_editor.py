from os.path import basename
from pyface.workbench.api import TraitsUIEditor
from pyface.api import FileDialog, CANCEL
from traits.api import Code, Instance, Str
from traitsui.api import CodeEditor, Group, Item, View
from traitsui.key_bindings import KeyBinding, KeyBindings
from traitsui.menu import NoButtons

from envisage.plugins.text_editor.editor.text_editor_handler import TextEditorHandler


def _id_generator():
    ''' A generator that returns the next number for untitled files. '''
    
    i = 1
    while True:
        yield(i)
        i += 1

    return

_id_generator = _id_generator()


class BNFEditor(TraitsUIEditor):

    key_bindings = Instance(KeyBindings) # The key bindings used by the editor
    text = Code
    wildcard = Str
    untitled_prefix='Untitled '

    def _obj_changed(self, new):
        ''' 
        
        Called by perform(self, event=None):
            self.window.workbench.edit(
                obj=File(''), 
                kind=LPPEditor,
                use_existing=False
            )
        
        ''' 
        if len(new.path) == 0:
            self.id   = self._get_unique_id()
            self.name = self.id
            
        else:
            self.id   = new.path
            self.name = basename(new.path)

            f = file(new.path, 'r')
            self.text = f.read()
            f.close()
    
    def _get_unique_id(self):
        """ Return a unique id for a new file. """
        prefix = self.untitled_prefix
        id = prefix + str(_id_generator.next())
        while self.window.get_editor_by_id(id) is not None:
            id = prefix + str(_id_generator.next())
        return id

    def _text_changed(self, trait_name, old, new):
        if self.traits_inited():
            self._dirty = True
    
    def _dirty_changed(self, dirty):
        if len(self.obj.path) > 0:
            if dirty:
                self.name = basename(self.obj.path) + '*'
            else:
                self.name = basename(self.obj.path)


    # 'TraitsUIEditor' interface.

    def create_ui(self, parent):
        ''' Creates the traits UI that represents the editor. '''
        ui = self.edit_traits(
            parent=parent, view=self._create_traits_ui_view(), kind='subpanel'
        )
        return ui

    
    # Methods

    def _create_traits_ui_view(self):
        ''' Create the traits UI view used by the editor.

        fixme: We create the view dynamically to allow the key bindings to be
        created dynamically (we don't use this just yet, but obviously plugins
        need to be able to contribute new bindings).

        '''
        from traitsui.api import TextEditor #TODO fails without error message
        view = View(
            Group(
                Item(
#                    'text', style='custom', editor=TextEditor(key_bindings=self.key_bindings)
                    'text', editor=CodeEditor(key_bindings=self.key_bindings) # doesn't work with TraitsUI 3.2.0
                ),
                show_labels = False
            ),
            id        = 'envisage.editor.text_editor', #CHANGE?
            handler   = TextEditorHandler(),
            kind      = 'live',
            resizable = True,
            width     = 1.0,
            height    = 1.0,
            buttons   = NoButtons,
        )    

        return view


    def _key_bindings_default(self):
        """ Trait initializer. """

        key_bindings = KeyBindings(
            KeyBinding(
                binding1    = 'Ctrl-s',
                description = 'Save the file',
                method_name = 'save'
            ),
#            KeyBinding(
#                binding1    = 'Ctrl-r',
#                description = 'Run the file',
#                method_name = 'run'
#            )
        )
        return key_bindings
        

    # 'IEditor' interface

    def save(self):
        ''' Saves the text to disk. '''
        if len(self.obj.path) == 0:
            self.save_as() # If the file has not yet been saved then save as
        else:
            f = file(self.obj.path, 'w')
            f.write(self.text)
            f.close()
            
            self._dirty = False

    def save_as(self):
        ''' Saves the text to disk after prompting for the file name. '''
        dialog = FileDialog(
            parent           = self.window.control,
            action           = 'save as',
            default_filename = self.name,
            wildcard         = self.wildcard
        )
        if dialog.open() != CANCEL:
            self.id   = dialog.path # Update the editor
            self.name = basename(dialog.path) # Update the editor
            self.obj.path = dialog.path # Update the resource
            self.save()
    
#    def run(self):
#        ''' Runs the file as Python. '''
#        self.save() # The file must be saved first!
#        # Execute the code.
#        if len(self.obj.path) > 0:
#            view = self.window.get_view_by_id(
#                'envisage.plugins.python_shell_view'
#            )
#            if view is not None:
#                view.execute_command(
#                    'execfile(r"%s")' % self.obj.path, hidden=False
#                )
    
    def select_line(self, lineno):
        ''' Selects the specified line. '''
        self.ui.info.text.selected_line = lineno
        return
    
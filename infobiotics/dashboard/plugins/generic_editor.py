from os.path import basename
from enthought.pyface.workbench.api import TraitsUIEditor
from enthought.pyface.api import FileDialog, CANCEL
from enthought.traits.api import Code, Instance
from enthought.traits.ui.api import CodeEditor, Group, Item, View
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings
from enthought.traits.ui.menu import NoButtons

def _id_generator():
    """ A generator that returns the next number for untitled files. """
    
    i = 1
    while True:
        yield(i)
        i += 1

    return

_id_generator = _id_generator()

class GenericEditor(TraitsUIEditor):

#    key_bindings = Instance(KeyBindings)

    def _obj_changed(self, obj):
        # The file will be the empty string if we are editing a file that has
        # not yet been saved.
        if len(obj.file) == 0:
            self.id   = self._get_unique_id()
            self.name = self.id
            if self.traits_inited():
                self._dirty = True
        else:
            self.id   = obj.file
            self.name = basename(obj.file)
#            f = file(obj.file, 'r')
#            self.text = f.read()
#            f.close()
        return

    def _get_unique_id(self, prefix=None):
        """ Return a unique id for a new set of parameters. """
        if prefix is None:
            prefix = self.obj.name

        id = prefix + str(_id_generator.next())
        while self.window.get_editor_by_id(id) is not None:
            id = prefix + str(_id_generator.next())
        return id

    def _dirty_changed(self, dirty):
        if len(self.obj.file) > 0:
            if dirty:
                self.name = basename(self.obj.file) + '*'
            else:
                self.name = basename(self.obj.file)
        return

    def create_ui(self, parent):
        return self.obj.edit_traits(kind='subpanel')#, parent=parent)
        
#    def _create_traits_ui_view(self):
#        return View(
#            Group(
#                Item(
#                    'text', editor=CodeEditor(key_bindings=self.key_bindings)
#                ),
#                show_labels = False
#            ),
#            id        = 'enthought.envisage.editor.text_editor',
#            handler   = TextEditorHandler(),
#            kind      = 'live',
#            resizable = True,
#            width     = 1.0,
#            height    = 1.0,
#            buttons   = NoButtons,
#        )    

#    def _key_bindings_default(self):
#        return KeyBindings(
#            KeyBinding(
#                binding1    = 'Ctrl-s',
#                description = 'Save the experiment parameters',
#                method_name = 'save'
#            ),
#            KeyBinding(
#                binding1    = 'Ctrl-p',
#                description = 'Perform the experiment',
#                method_name = 'perform'
#            ),
#            KeyBinding(
#                binding1    = 'Ctrl-z',
#                description = 'Undo the last change',
#                method_name = 'undo'
#            ),
#            KeyBinding(
#                binding1    = 'Ctrlyr',
#                description = 'Redo the last change',
#                method_name = 'redo'
#            ),
#        )
#    
#    def save(self):
#        print 'save'
#    def perform(self):
#        print 'perform'
#    def undo(self):
#        print 'undo'
#    def redo(self):
#        print 'redo'
    

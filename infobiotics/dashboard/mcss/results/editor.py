from os.path import basename
from enthought.pyface.workbench.api import Editor
from enthought.pyface.api import FileDialog, CANCEL
from enthought.traits.api import Code, Instance
from enthought.traits.ui.api import CodeEditor, Group, Item, View
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings
from enthought.traits.ui.menu import NoButtons
from PyQt4.QtCore import QObject, SIGNAL
import os.path

def _id_generator():
    """ A generator that returns the next number for untitled files. """
    
    i = 1
    while True:
        yield(i)
        i += 1

    return

_id_generator = _id_generator()

class McssResultsEditor(Editor):

    obj_filename_change_notifier = Instance(QObject)

    def obj_filename_changed(self, filename):
        self.name = os.path.basename(filename)        

    def _obj_changed(self, obj):
        self.id = self._get_unique_id()
        if hasattr(obj, 'filename'):
            self.name = os.path.basename(obj.filename) 
        else:
            self.name = self.id
        self.obj_filename_change_notifier = QObject()
        self.obj_filename_change_notifier.connect(obj, SIGNAL('filename_changed'), self.obj_filename_changed)
        if self.traits_inited():
            self._dirty = True

    def _get_unique_id(self, prefix=None):
        """ Return a unique id for a new set of parameters. """
        if prefix is None:
            prefix = 'Simulation '

        id = prefix + str(_id_generator.next())
        while self.window.get_editor_by_id(id) is not None:
            id = prefix + str(_id_generator.next())
        return id
    
    def create_control(self, parent):
        return self.obj
    

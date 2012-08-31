from os.path import basename
from pyface.workbench.api import Editor
from pyface.api import FileDialog, CANCEL
from traits.api import Code, Instance
from traitsui.api import CodeEditor, Group, Item, View
from traitsui.key_bindings import KeyBinding, KeyBindings
from traitsui.menu import NoButtons
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
        if not obj:
            return
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
    

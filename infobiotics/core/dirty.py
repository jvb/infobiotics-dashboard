'''

Calling configure_traits (or edit_traits) should make '_interaction_mode' True.

jvb@weasel:~/dashboard/infobiotics/core$ python dirty.py
script
jvb@weasel:~/dashboard/infobiotics/core$ python -c 'import dirty; t = dirty.Test(); print t._interaction_mode'
terminal
jvb@weasel:~/dashboard/infobiotics/core$ python -i dirty.py
terminal

'''

from enthought.traits.ui.api import Controller, View
from enthought.traits.api import HasTraits, Bool, Button, ListStr, Str, Instance, Enum

class Handler(Controller):

    title = Str

    def init(self, info):
        self.title = info.ui.title

#    def setattr(self, info, object, name, value):
#        super(Handler, self).setattr(info, object, name, value)
#        if name in object._names:
#            info.object._dirty = True

    def object__dirty_changed(self, info):
        if info.initialized:
            if info.object._dirty:
                info.ui.title = self.title + '*'
            else:
                info.ui.title = self.title

    view = View(
        'switch1', 'switch2',
        '_save', '_load',
        title='Title',
        buttons=['OK', 'Cancel'],
        id='test',
    )

class Test(HasTraits):
    switch1 = Bool
    switch2 = Bool
    _dirty = Bool(False)
    _save = Button
    _load = Button
    _names = ListStr(['switch1', 'switch2'])
    _interaction_mode = Enum(['script', 'terminal', 'gui'])

    def __interaction_mode_default(self):
        import sys
        import __main__
        if sys.flags.interactive or not hasattr(__main__, '__file__'):
            return 'terminal'
        else:
            return 'script'
    
    def _anytrait_changed(self, name, old, new): # instead of setattr on handler
        if name in self._names:
            self._dirty = True
    
    def __load_changed(self):
        self.load()
        
    def load(self, force=False):
        if self._dirty and not force:
            if self._interaction_mode == 'gui':
#                print 'message box'
                from enthought.traits.ui.message import auto_close_message, error, message
                if message(str('Save parameters before continuing?'), title='Unsaved parameters', buttons=['OK', 'Cancel']):
                    self.save() #TODO need to call handler's save method either from here or in save
            elif self._interaction_mode == 'terminal':
                print 'command line prompt'
            else:
                print 'log overwriting unsaved parameters'
    
    def save(self):
        self._dirty = False
    
    def __save_changed(self):
        self.save()
        
    handler = Instance(Handler)
    def _handler_default(self):
        return Handler(model=self)
    
    def configure(self, **kwargs):
        interaction_mode = self._interaction_mode # remember previous mode of interaction
        self._interaction_mode = 'gui' # set mode of interaction
        self.handler.configure_traits(**kwargs)
        self._interaction_mode = interaction_mode # restore previous mode of interaction


if __name__ == '__main__':
    t = Test()
    t.configure()

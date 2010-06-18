from infobiotics.common.api import ParamsHandler#TODO ExperimentHandler?
from enthought.traits.api import (
    Int, #Button, Property, Str, on_trait_change,
)
#from infobiotics.commons.traits.api import Percentage
from enthought.traits.ui.api import (
    View, Item, #DefaultOverride, TextEditor,                      
)
from infobiotics.commons.traits.ui.qt4.cancellable_progress_editor import CancellableProgressEditor

#class CancelExperimentMixin(object):
#    ''' Mixin '''
#    cancel = Button
#    
#    @on_trait_change('cancel')
#    def cancelled(self):
#        print 'cancelled'

class ExperimentProgressHandler(ParamsHandler):#, CancelExperimentMixin):
    ''' TODO shouldn't this derive from ExperimentHandler? '''
    
#    progress = Property(Percentage) # subclasses must repeat this line!?
#    def _get_progress(self):
#        raise NotImplementedError
#    def _set_progress(self): # only need when progress being edited with a RangeEditor
#        return
    progress = Int

    traits_view = View(
#        Item('handler.progress', editor=DefaultOverride(low_label='0%', high_label='100%', format='%2.1f')),
#        Item('handler.progress', editor=TextEditor()),
#        Item('handler.status', style='readonly', visible_when='len(handler.status) > 0'),
#        Item('handler.cancel'),
        Item('progress', 
            editor=CancellableProgressEditor(
                #TODO link to min, max, title, message, cancel, etc.
            ),
        ),
    )

    def object_finished_changed(self, info):
        ''' Listens for finished event on experiment and closes itself, calling 
        the superclasses _on_close method. TODO why? '''
        if self.close(info, True):
            self._on_close(info)

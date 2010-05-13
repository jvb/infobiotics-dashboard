from infobiotics.common.api import ParamsHandler
from enthought.traits.api import (
    Button, Property, Str, on_trait_change,
)
from infobiotics.commons.traits.api import Percentage
from enthought.traits.ui.api import (
    View, Item, DefaultOverride, TextEditor,                      
)

#class CancelExperimentMixin(object):
#    ''' Mixin '''
#    cancel = Button
#    
#    @on_trait_change('cancel')
#    def cancelled(self):
#        print 'cancelled'

class ExperimentProgressHandler(ParamsHandler):#, CancelExperimentMixin):
    
    progress = Property(Percentage) # subclasses must repeat this line!?
    
    def _get_progress(self):
        raise NotImplementedError
    
    def _set_progress(self): # only need when progress being edited with a RangeEditor
        return

    traits_view = View(
#        Item('handler.progress', editor=DefaultOverride(low_label='0%', high_label='100%', format='%2.1f')), #FIXME         Item('handler.progress', editor=DefaultOverride(low_label='0%', high_label='100%', format='%2.1f')),
        Item('handler.progress', editor=TextEditor()),
        Item('handler.status', style='readonly', visible_when='len(handler.status) > 0'),
#        Item('handler.cancel'),
    )

    def object_finished_changed(self, info):
        if self.close(info, True):
            self._on_close(info)

from infobiotics.common.api import ParamsHandler
from enthought.traits.api import (
    Button, Property, Str, on_trait_change,
)
from commons.traits.api import Percentage
from enthought.traits.ui.api import (
    View, Item, DefaultOverride,                              
)

class CancelExperimentMixin(object):
    ''' Mixin '''
    cancel = Button
    
    @on_trait_change('cancel')
    def cancelled(self):
        print 'cancelled'

class ExperimentProgressHandler(ParamsHandler):#, CancelExperimentMixin):
    
    progress = Property(Percentage) # subclasses must repeat this line!?
    status = Property(Str)
    
    def _get_progress(self):
        raise NotImplementedError
    
    def _set_progress(self): # only need when progress being edited with a RangeEditor
        return

    def _get_status(self):
        return ''
        
    traits_view = View(
        Item('controller.progress', editor=DefaultOverride(low_label='0%', high_label='100%', format='%2.1f')),
        Item('controller.status', style='readonly', visible_when='len(controller.status) > 0'),
#        Item('controller.cancel'),
    )

    def object_finished_changed(self, info):
        print 'ExperimentProgressHandler.object_finished_changed(self, info)'

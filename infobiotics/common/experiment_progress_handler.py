from enthought.traits.api import (
    Button, Property, Str, on_trait_change,
)
from infobiotics.common.api import ParamsHandler, percentage
from enthought.traits.ui.api import (
    View, Item, DefaultOverride,                              
)

class CancelExperimentMixin(object):
    ''' Mixin '''
    cancel = Button
    
    @on_trait_change('cancel')
    def cancelled(self):
        pass

class ExperimentProgressHandler(ParamsHandler):#, CancelExperimentMixin):
    
    progress = Property(percentage) # subclasses must repeat this line!?
    status = Property(Str)

    def _get_progress(self):
        raise NotImplementedError
    
    def _get_status(self):
        raise NotImplentedError
    
#    def model_finished_fired(self):
#        print 'finished'

    traits_view = View(
        Item('controller.progress', editor=DefaultOverride(low_label='0%', high_label='100%', format='%2.1f')),
        'controller.status',
    )
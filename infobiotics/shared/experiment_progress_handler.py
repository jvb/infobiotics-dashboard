from infobiotics.shared.api import \
    ParamsHandler, Property, percentage, Str, View, Item, DefaultOverride

class ExperimentProgressHandler(ParamsHandler):
    
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
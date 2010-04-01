from infobiotics.shared.api import \
    ModelView, Property, percentage, Str, View, Item, DefaultOverride

class ExperimentProgressHandler(ModelView): # --> Mixin?
    
    progress = Property(percentage) # subclasses must repeat this line!?
    status = Property(Str)

    def _get_progress(self):
        raise NotImplementedError
    
    def _get_status(self):
        raise NotImplentedError
    
    traits_view = View(
        Item('progress', editor=DefaultOverride(low_label='0%', high_label='100%', format='%2.1f')),
        'status',
    )

#    def model_finished_fired(self):
#        print 'finished'

    def model_title_changed(self, info):
        info.ui.title = info.model.title
        
    def _progress_changed(self, progress):
        print progress
        
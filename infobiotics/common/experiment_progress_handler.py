from enthought.traits.ui.api import Controller, View, Item
from enthought.traits.api import Int, Str, Bool, Callable 
from infobiotics.commons.traits.ui.qt4.cancellable_progress_editor import CancellableProgressEditor

class ExperimentProgressHandler(Controller):
    '''
    self.model == info.object == Instance(Experiment)
    '''
    
    progress = Int

    # traits controlling presentation of progress 
    title = Str
    message = Str
    min = Int(0)
    max = Int(0)
    show_time = Bool(False)
#    cancel = Callable #TODO
    
    def init(self, info):
        self.info.ui.title = self.model.handler.title
    
    def _progress_changed(self):
        print self.min, self.max, self.show_time
        print self.progress
    
    traits_view = View(
#        Item('handler.progress', 
        Item('progress', 
            show_label=False,
            editor=CancellableProgressEditor(
#                title='Title',
                    title_name='title',
#                message='Message',
                    message_name='handler.message',
#                min=0,
                    min_name='min',
                max=100,
#                    max_name='max',
#                show_text=False,
                show_percent = True,
#                show_time = True,
#                    show_time_name = 'show_time', # overrides show_time above
                show_max = True,
                show_value = True,
#                prefix_message=True,
                can_cancel=False, 
#                cancelled=cancel,
            ),
        ),
        width=250,
    )

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
        if self.close(info, True):
            self._on_close(info)

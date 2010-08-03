from enthought.traits.ui.api import Controller, View, VGroup, Item
from enthought.traits.api import Int, Str, Bool, Callable 
from infobiotics.commons.traits.ui.qt4.cancellable_progress_editor import CancellableProgressEditor

class ExperimentProgressHandler(Controller):
    '''
    self.model == info.object == Instance(Experiment)
    '''
    
    progress = Int

    # traits controlling presentation of progress 
    message = Str
    max = Int(0)
    
    def init(self, info):
        self.info.ui.title = self.model.handler.title
    
    def _progress_changed(self, info):
        print info #FIXME
        print self.min, self.max, self.show_time
        print self.progress
    
    traits_view = View(
        VGroup(
            Item('handler.progress',
                show_label=False,
                editor=CancellableProgressEditor(
                    title_name='title',
                    message_name='message',
                    min=0,
                    min_name='min',
                    max=0,
                    max_name='max',
                    show_text=False,
                    show_percent=False,
                    show_time=False,
    #                show_time_name='show_time', # overrides show_time above
                    show_max=False,
                    show_value=False,
                    prefix_message=False,
                    can_cancel=False,
    #                cancelled=cancel,
                ),
            ),
            show_border=True,
        ),
        width=250,
    )

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
        if self.close(info, True):
            self._on_close(info)

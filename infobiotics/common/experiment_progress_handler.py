from enthought.traits.ui.api import Controller, View, Item
from enthought.traits.api import Int, Str, Callable, Bool
from infobiotics.commons.traits.ui.qt4.cancellable_progress_editor import CancellableProgressEditor

class ExperimentProgressHandler(Controller):
    
    progress = Int

    # traits controlling presentation of progress 
    title = Str
    message = Str
    min = Int(0)
    max = Int(0)
#    cancel = Callable
#    show_time = Bool(False)
    
    def init(self, info):
        self.info.ui.title = self.model.handler.title
    
    traits_view = View(
        Item('handler.progress', 
            show_label=False,
            editor=CancellableProgressEditor(
#                title='Title',
                    title_name='title',
#                message='Message',
                    message_name='message',
#                min=0,
                    min_name='min',
#                max=100,
                    max_name='max',
#                show_text=False,
                show_percent = True,
                can_cancel=False, 
#                cancelled=cancel,
                show_time = False,
                    show_time_name = 'show_time', # overrides show_time above
                show_max = False,
                show_value = False,
#                prefix_message=True,
            ),
        ),
    )

    def object_finished_changed(self, info):
        ''' Triggered when experiment's expect loop finishes. '''
        if self.close(info, True):
            self._on_close(info)

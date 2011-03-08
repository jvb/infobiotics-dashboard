#FIXME adapt for ExperimentHandler and then remove

from enthought.traits.ui.api import Controller, View, VGroup, Item
from enthought.traits.api import Str, Button 
from infobiotics.commons.traits.ui.qt4.progress_editor import ProgressEditor                

class ExperimentProgressHandler(Controller):
    '''
    self.model == info.object == Instance(Experiment)
    '''

    # traits used by ProgressEditor 
    title = Str('title')
    message = Str('message')
    cancel = Button
    
    def init(self, info):
        pass
#        info.ui.title = 'Running experiment' 
#        self.title = self.model.executable_name
#        self.message = self.model.params_file
    
    def _cancel_changed(self):
        #TODO are you sure?
        self.info.ui.dispose()
        self.model.cancel()
    
    traits_view = View(
        VGroup(
            Item('object._progress_percentage',
                show_label=False,
                editor=ProgressEditor(
                    title_name='title',
                    message_name='message',
                    min=0,
                    max=100,
#                    show_title=True,
#                    show_message=True,
                    show_text=True,
                    show_percent=False,
                    show_time=True,
                    show_max=True,
                    show_value=True,
                    prefix_message=True,
                ),
            ),
            Item('handler.cancel', show_label=False),
            show_border=True,
        ),
        width=250,
    )

#    def init(self, info):
#        info.ui.title = info.object._handler.title
        
#    def object_finished_changed(self, info): # sometimes this isn't called
#        ''' Triggered when experiment's expect loop finishes. '''
##        print self
##        if self.close(info, True):
##            self._on_close(info)
#        info.ui.dispose()


if __name__ == '__main__':
    execfile('experiment.py')

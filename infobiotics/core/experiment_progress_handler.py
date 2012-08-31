#FIXME adapt for ExperimentHandler and then remove

from enthought.traits.ui.api import Controller, View, VGroup, Item
from enthought.traits.api import Str, Button 
from infobiotics.commons.traits.ui.qt4.progress_editor import ProgressEditor                
from enthought.pyface.api import YES, NO, confirm

class ExperimentProgressHandler(Controller):
    '''
    self.model == info.object == Instance(Experiment)
    '''

    # traits used by ProgressEditor 
    cancel = Button
    
    def init(self, info):
        self.info = info
        info.ui.title = 'Experiment in progress' 
    
    def _cancel_changed(self):
        if confirm(None, 'Are you sure you want to stop the experiment?', title='Really cancel?') == YES:
            self.model.cancel()
            self.info.ui.dispose()

    traits_view = View(
        VGroup(
            Item('object._progress_percentage',
                show_label=False,
                editor=ProgressEditor(
                    title_name='object.executable_name',
                    message_name='object.message',
                    min=0,
                    max=100,
                    show_text=True,
                    show_percent=True,
                    show_time=True,
                    show_max=True,
                    show_value=True,
                    prefix_message=False,
                ),
            ),
            Item('controller.cancel', show_label=False),
            show_border=True,
        ),
        width=250,
    )

#    def object_finished_changed(self, info): # sometimes this isn't called
#        ''' Triggered when experiment's expect loop finishes. '''
##        print self
##        if self.close(info, True):
##            self._on_close(info)
#        info.ui.dispose()


if __name__ == '__main__':
    execfile('experiment.py')

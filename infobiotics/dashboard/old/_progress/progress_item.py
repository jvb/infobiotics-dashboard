from progress_meter import *
from traits.api import Instance
from traitsui.api import View, Item, CustomEditor, HGroup, VGroup
from PyQt4.QtGui import QProgressBar

class ProgressItem(ProgressMeter):
    ''' A progress bar with customisable interactions.  

    ...

    When min and max are both zero (the default) the progress percentage is not
    shown, instead the progress bar bounces back and forth. 

    ProgressItem can be customised and used in two ways, by direct 
    instantiation or by subclassing to override more fundamental aspects of the
    default behaviour.

    Instantiation:
        ProgressItem(
            title='title', 
            text='text', 
            min=0, 
            max=10, 
            start_condition='object.progress == object.min', 
            hide_function=lambda this: self.experiments.remove(this)
        )

    Subclassing:
        class ExperimentProgressItem(ProgressItem):
            title = 'title'
            text = 'text'
            def _cancel_function_default(self):
                return ...
                
    '''

    progress_bar = Instance(QProgressBar, None)

    def _progress_bar_default(self):
        progress_bar = QProgressBar()
        progress_bar.setMinimum(self.min)
        progress_bar.setMaximum(self.max)
        return progress_bar 

    def _progress_bar_factory_function(self, window_parent, editor, *args, **kwargs):
        ''' Returns a QProgressBar widget for a TraitsUI window. 
        
        Used by CustomEditor(factory=_progress_bar_factory_function, args=('tuple',)
        
        Can't just return self.progress_bar one should be should be created 
        here and then set.
        
        window_parent = <PyQt4.QtGui.QBoxLayout object at ...>
        editor = <traitsui.qt4.custom_editor.CustomEditor object at ...>
        
        '''
        progress_bar = QProgressBar()
        progress_bar.setMinimum(self.min)
        progress_bar.setMaximum(self.max)
        self.progress_bar = progress_bar
        return progress_bar 
    
    def _min_changed(self):
        self.progress_bar.setMinimum(self.min)
    
    def _max_changed(self):
        self.progress_bar.setMaximum(self.max)

    def _value_changed(self, value):
        self.progress_bar.setValue(value)
    
    def additional_buttons(self):
        ''' Should return a tuple of Item and Group objects. '''
        return tuple()

    def traits_view(self):
        return View(
            VGroup(
                Item('title',
                    show_label=False,
                    style='readonly',
                    visible_when='len(object.title) > 0',
                    emphasized=True, 
                ),
    
#                Item('text', 
#                    show_label=False,
#                    style='readonly',
#                    visible_when='len(object.text) > 0',
#                ),
    
                Item('_text', 
                    show_label=False,
                    style='readonly',
                    visible_when='len(object._text) > 0',
                ),
    
                Item('progress_bar', 
                    style='custom',
                    show_label=False, 
                    editor=CustomEditor(
                        factory=self._progress_bar_factory_function,
                    ),
#                    visible_when='object.min < object.value < object.max',
                ),
    
                HGroup(
                    Item('start',
                        show_label=False,
                        visible_when=self.start_condition,
                        enabled_when=self.start_condition,
                    ),
                    
                    Item('pause',
                        show_label=False,
                        visible_when=self.pause_condition,
                        enabled_when=self.pause_condition,
                    ),
                    
                    Item('continue_',
                        show_label=False,
                        visible_when=self.continue_condition,
                        enabled_when=self.continue_condition,
                    ),
                    
                    Item('cancel',
                        show_label=False,
                        visible_when=self.cancel_condition,
                        enabled_when=self.cancel_condition,
                    ),
    
                    Item('retry',
                        show_label=False,
                        visible_when=self.retry_condition,
                        enabled_when=self.retry_condition,
                    ),
                        
                    Item('hide',
                        show_label=False,
                        visible_when=self.hide_condition,
                        enabled_when=self.hide_condition,
                    ),
                    
                    self.additional_buttons(),
                ),
                
#                Item('_'),
            )
        )

#    # debugging
#    def _anytrait_changed(self, name, old, new):
#        print name, old, new

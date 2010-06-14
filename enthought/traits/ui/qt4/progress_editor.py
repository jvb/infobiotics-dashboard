import os; os.environ['ETS_TOOLKIT']='qt4'
import time
from enthought.traits.api import Instance
from enthought.traits.ui.qt4.editor import Editor
#from PyQt4.QtCore import *
from PyQt4.QtGui import (
    QWidget, QVBoxLayout, QProgressBar, QHBoxLayout, QDialogButtonBox, QLabel, 
)
from PyQt4.QtCore import SLOT, SIGNAL

class SimpleEditor(Editor):
    """
    Show a progress bar with all the optional goodies

    """
    
    progress_bar = Instance(QProgressBar)
    
    def init(self, parent):
#        title=self.factory.title
#        message=self.factory.message
#        min=self.factory.min
#        max=self.factory.max
#        can_cancel=self.factory.can_cancel
#        show_time=self.factory.show_time
#        show_percent=self.factory.show_percent

#        message_trait?
#        min_trait?
#        max_trait?
#        show_value_and_max? 

        self.control = self._create_control(parent)
        self.set_tooltip()
        self.reset()

    def _create_control(self, parent):
        layout = QVBoxLayout()
        
        if len(self.factory.message) > 0:
            label = QLabel(self.factory.message)
            layout.addWidget(label)
    
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(self.factory.min, self.factory.max)
        
        if self.factory.can_cancel:
            buttons = QDialogButtonBox()
            buttons.addButton(u'Cancel', QDialogButtonBox.RejectRole)
            buttons.connect(buttons, SIGNAL('rejected()'), self.cancelled)
            layout2 = QHBoxLayout()
            layout2.addWidget(self.progress_bar)
            layout2.addWidget(buttons)
            layout.addLayout(layout2)
        else:
            layout.addWidget(self.progress_bar)
        
        if self.factory.show_time:
            self._elapsed_control = self._create_time_label(layout, "Elapsed time: ")
            self._estimated_control = self._create_time_label(layout, "Estimated time: ")
            self._remaining_control = self._create_time_label(layout, "Remaining time: ")
        
        if self.factory.show_percent:
#            self.progress_bar.setTextVisible()
            self.progress_bar.setFormat('%p%')
        else:
            self.progress_bar.setFormat('%v/%m')
            self.progress_bar.setFormat('%p% (%v/%m)')
            
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def cancelled(self):
        print 'cancelled' #TODO accept a callable 'cancel' trait

    def _create_time_label(self, layout, text):
        dummy = QLabel(text)
#        dummy.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        label = QLabel('unknown')
        layout2 = QHBoxLayout()
        layout2.addWidget(dummy)
        layout2.addWidget(label)
        layout.addLayout(layout2)
        return label

    def _set_time_label(self, value, control):
        hours = value / 3600
        minutes = (value % 3600) / 60
        seconds = value % 60
        label = "%1u:%02u:%02u" % (hours, minutes, seconds)
        control.setText(control.text()[:-7] + label)

    def update_editor(self):
        if self.factory.min <= self.value <= self.factory.max:
            if self.value == self.factory.min:
                self.reset()
            self.progress_bar.setValue(self.value)

        if self.factory.show_time:
            if (self.factory.max != self.factory.min):
                percent = (float(self.value) - self.factory.min)/(self.factory.max - self.factory.min)
            else:
                percent = 1.0
            if self.factory.show_time and (percent != 0):
                current_time = time.time()
                elapsed = current_time - self._start_time
                estimated = elapsed/percent
                remaining = estimated - elapsed
                self._set_time_label(elapsed, self._elapsed_control)
                self._set_time_label(estimated, self._estimated_control)
                self._set_time_label(remaining, self._remaining_control)            

    def reset(self):
        self.progress_bar.reset()
        self._start_time = time.time()


if __name__ == '__main__':
    
    import os; os.environ['ETS_TOOLKIT']='qt4'
    from enthought.traits.api import HasTraits, Int, Button
    from enthought.traits.ui.api import ProgressEditor, View, Item
    
    class Test(HasTraits):
        progress = Int
        go = Button
        
        def _go_fired(self):
            import time
            for i in range(101):
                self.progress = i
                time.sleep(0.05)
        
        view = View(
            Item('go', show_label=False),
            Item('progress', 
                editor=ProgressEditor(
                    can_cancel=True,
                    message='message',
                    show_percent = True,
                    show_time = True,
                    min=0,
                    max=100,
                )
            ),
        )
        
    Test().configure_traits()
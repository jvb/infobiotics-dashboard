from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import Instance
from enthought.traits.ui.qt4.editor import Editor
from PyQt4.QtGui import (
    QWidget, QVBoxLayout, QProgressBar, QDialogButtonBox, QLabel, QGridLayout,  
)
from PyQt4.QtCore import SLOT, SIGNAL
import time

class SimpleEditor(Editor):

    def init(self, parent):
        self.control = self._create_control(parent)
        self.set_tooltip()
        self.reset()

    def _create_control(self, parent):
        layout = QVBoxLayout()
        
        if len(self.factory.title) > 0:
            title = QLabel('<B>%s</B>' % self.factory.title)
            layout.addWidget(title)
    
        if len(self.factory.message) > 0:
            message = QLabel(self.factory.message)
            layout.addWidget(message)
    
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(self.factory.min, self.factory.max)
        layout.addWidget(self._progress_bar)
        
        if self.factory.show_time:
            elapsed_label = QLabel('Elapsed time:')
            estimated_label = QLabel('Estimated time:')
            remaining_label = QLabel('Remaining time:')
            self._elapsed_control = QLabel('unknown')
            self._estimated_control = QLabel('unknown')
            self._remaining_control = QLabel('unknown')
            grid_layout = QGridLayout()
            grid_layout.addWidget(elapsed_label, 0, 0)
            grid_layout.addWidget(self._elapsed_control, 0, 1)
            grid_layout.addWidget(estimated_label, 1, 0)
            grid_layout.addWidget(self._estimated_control, 1, 1)
            grid_layout.addWidget(remaining_label, 2, 0)
            grid_layout.addWidget(self._remaining_control, 2, 1)
            grid_layout.setColumnStretch(1, 1)
            layout.addLayout(grid_layout)
        
        if self.factory.show_percent:
            self._progress_bar.setFormat('%p%')
        else:
            self._progress_bar.setFormat('%v/%m')
#            self._progress_bar.setFormat('%p% (%v/%m)')

#        if self.factory.hide_text:
#            self._progress_bar.setTextVisible(False)
            
        widget = QWidget()
        widget.setLayout(layout)
        return widget

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
            self._progress_bar.setValue(self.value)

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
        self._progress_bar.reset()
        self._start_time = time.time()


if __name__ == '__main__':
    
    import os; os.environ['ETS_TOOLKIT']='qt4'
    from enthought.traits.api import HasTraits, Int, Button
    from enthought.traits.ui.api import ProgressEditor, View, Item, HGroup, Spring
    
    class Test(HasTraits):
        progress = Int
        go = Button
        
        def _go_fired(self):
            import time
            for i in range(101):
                self.progress = i
                time.sleep(0.05)
        
        view = View(
            Item('progress', 
                show_label=False,
                editor=ProgressEditor(
                    title='title',
                    message='message',
                    show_percent = True,
                    show_time = True,
                    min=0,
                    max=100,
                    can_cancel=True,
                )
            ),
            HGroup(
                Spring(),
                Item('go', show_label=False),
            ),
            resizable=True, 
        )
        
    Test().configure_traits()
    
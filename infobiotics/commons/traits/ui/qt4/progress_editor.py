from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import Callable, Int, Unicode, Bool, Str, on_trait_change, Undefined
from enthought.traits.ui.qt4.editor import Editor
from enthought.traits.ui.api import BasicEditorFactory
from PyQt4.QtGui import (
    QWidget, QVBoxLayout, QProgressBar, QDialogButtonBox, QLabel, QGridLayout,
#    QTextEdit, 
)
from PyQt4.QtCore import SIGNAL
import time

class _ProgressEditor(Editor):

    title = Unicode   # synced from factory.title_name 
    message = Unicode # synced from factory.message_name
    min = Int#Float   # synced from factory.min_name
    max = Int#Float   # synced from factory.max_name
    show_time = Bool  # synced from factory.show_time_name

    def _title_changed(self):
        if self._title is not None:
            self._title.setText('<B>%s</B>' % self.title)
            self._title.setVisible(len(self.title) > 0)
    
    def _message_changed(self):
        if self._message is not None:
            self._message.setText(self.message)
            self._message.setVisible(len(self.message) > 0)
        if self.factory.prefix_message:
            self.set_text()

    def _show_time_changed(self):
        if self._time_widget is not None:
            self._time_widget.setVisible(self.show_time)
    
    @on_trait_change('min, max')
    def change_range(self):
        if self._progress_bar is not None:
            self._progress_bar.setRange(self.min, self.max)
            self.update_editor()
    
    def init(self, parent):

        self.title = self.factory.title
        if len(self.factory.title_name) > 0:
            self.sync_value(self.factory.title_name, 'title')#, 'from')
        
        self.message = self.factory.message
        if len(self.factory.message_name) > 0:
            self.sync_value(self.factory.message_name, 'message')#, 'from')

        self.min = self.factory.min
        if len(self.factory.min_name) > 0:
            self.sync_value(self.factory.min_name, 'min')#, 'from')

        self.max = self.factory.max
        if len(self.factory.max_name) > 0:
            self.sync_value(self.factory.max_name, 'max')#, 'from')
        
        self.show_time = self.factory.show_time
        if len(self.factory.show_time_name) > 0:
            self.sync_value(self.factory.show_time_name, 'show_time')#, 'from')
        
        self.control = self._create_control(parent)

        self.set_tooltip()
        self.reset()

    def _create_control(self, parent):
        layout = QVBoxLayout()
        
        if len(self.title) > 0:
            self._title = QLabel('<B>%s</B>' % self.title)
            layout.addWidget(self._title)
    
        if not self.factory.prefix_message and len(self.message) > 0:
            self._message = QLabel(self.message)
#            self._message = QTextEdit(self.message)
#            self._message.setReadOnly(True)
            layout.addWidget(self._message)
    
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(self.min, self.max)
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
            self._time_widget = QWidget()
            self._time_widget.setLayout(grid_layout)
            layout.addWidget(self._time_widget)
        
        if self.factory.show_text:
            self.set_text()
        else:
            self._progress_bar.setTextVisible(False)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def set_text(self):
        if self._progress_bar is None:
            return
        if self.factory.prefix_message:
            format = self.message + ' '
        else:
            format = ''
        if self.factory.show_value:
            format += '%v'
        if self.factory.show_max:
            if self.factory.show_value:
                format += '/'
            format += '%m'
        if self.factory.show_value or self.factory.show_max:
            format += ' '
        if self.factory.show_percent:
            if self.factory.show_value or self.factory.show_max:
                format += '(%p%)'
            else:
                format += '%p%'
        self._progress_bar.setFormat(format)

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
            if self.value != Undefined: 
                self._progress_bar.setValue(self.value)
            if self.factory is not None and self.factory.show_time:
                if (self.factory.max != self.factory.min):
                    percent = (float(self.value) - self.factory.min) / (self.factory.max - self.factory.min)
                    # if float(<undefined>) raises an error here then probably the
                    # name of the trait this is editing is mispelled or owned by
                    # the handler, e.g. 'handler.progress' instead of 'progress'. 
                else:
                    percent = 1.0
                if self.factory.show_time and (percent != 0):
                    current_time = time.time()
                    elapsed = current_time - self._start_time
                    estimated = elapsed / percent
                    remaining = estimated - elapsed
                    self._set_time_label(elapsed, self._elapsed_control)
                    self._set_time_label(estimated, self._estimated_control)
                    self._set_time_label(remaining, self._remaining_control)            

    def reset(self):
        self._progress_bar.reset()
        self._start_time = time.time()


class ProgressEditor(BasicEditorFactory):
    klass = _ProgressEditor

    min = Int
    max = Int
    title = Unicode
    message = Unicode
    show_text = Bool(True)
    show_percent = Bool(True)
    show_value = Bool(True)
    show_max = Bool(True)
    show_time = Bool(False)
    title_name = Str
    message_name = Str
    min_name = Str
    max_name = Str
    show_time_name = Str
    prefix_message = Bool(False, desc='whether to prefix message to progress bar text')


if __name__ == '__main__':
    
    import os; os.environ['ETS_TOOLKIT'] = 'qt4'
    from enthought.traits.api import HasTraits, Int, Button
    from enthought.traits.ui.api import View, Item, HGroup, Spring, Handler
#    from infobiotics.commons.traits.ui.qt4.progress_editor import ProgressEditor
    
    class ClosingHandler(Handler):
        def object_cancel_changed(self, info):
            info.ui.dispose()
    
    class Test(HasTraits):
        progress = Int
        title = Str('title')
        message = Str('message')
        min = Int
        max = Int(100)
        
        go = Button
        
        def _go_fired(self):
            import time
            for i in range(101):
                self.progress = i
                time.sleep(0.025)

        cancel = Button
        
        def _cancel_fired(self):
            print 'got here'
        
        view = View(
            Item('title'),
            Item('message'),
            HGroup(
                Item('min'),
                Item('max'),
            ),
            Item('progress',
                show_label=False,
                editor=ProgressEditor(
                    title='Title',
                    title_name='title',
                    message='Message',
                    message_name='message',
                    min=0,
                    min_name='min',
                    max=100,
                    max_name='max',
#                    show_text=False,
                    show_percent=True,
                    show_time=True,
                    show_max=False,
                    show_value=False,
                    prefix_message=True,
                ),
            ),
            HGroup(
                Spring(),
                Item('go', show_label=False),
            ),
            Item('cancel', show_label=False),
            resizable=True,
            handler=ClosingHandler
        )
        
    Test().configure_traits()

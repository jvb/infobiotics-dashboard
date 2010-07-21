from enthought.etsconfig.etsconfig import ETSConfig
ETSConfig.toolkit = 'qt4'

from PyQt4 import QtGui, QtCore

from enthought.traits.api import Float, Any, Str, Trait
from enthought.traits.ui.editors.api import RangeEditor
from enthought.traits.ui.qt4.editor import Editor
from enthought.traits.ui.qt4.extra.range_slider import RangeSlider

class _BoundsEditor(Editor):

    evaluate = Any

    min = Any
    max = Any
    low = Any
    high = Any
    format = Str

    def init(self, parent):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        
        
        factory = self.factory

#        trait = self.object.trait(self.item.name)
#        if not factory.min:
#            self.min = trait.handler._low #TODO

#        if not factory.min_name:
#            self.min = factory.min
#        self.sync_value(factory.min_name, 'min', 'both')
#
#        if not factory.max_name:
#            self.max = factory.max
#        self.sync_value(factory.max_name, 'max', 'both')

        if not factory.low_name:
            self.low = factory.low
        self.sync_value(factory.low_name, 'low', 'both')

        if not factory.high_name:
            self.high = factory.high
        self.sync_value(factory.high_name, 'high', 'both')

        self.format = factory.format
        #TODO format_name

        self.evaluate = factory.evaluate
        self.sync_value(factory.evaluate_name, 'evaluate', 'from')

        self.control = QtGui.QWidget()
        panel = QtGui.QHBoxLayout(self.control)
        panel.setMargin(0)

        self._label_lo = QtGui.QLineEdit(self.format % self.low)
        QtCore.QObject.connect(self._label_lo, QtCore.SIGNAL('editingFinished()'),
                self.update_low_on_enter)
        panel.addWidget(self._label_lo)

        # The default size is a bit too big and probably doesn't need to grow.
        sh = self._label_lo.sizeHint()
        sh.setWidth(sh.width() / 2)
        self._label_lo.setMaximumSize(sh)

        self.control.slider = slider = RangeSlider(QtCore.Qt.Horizontal)
        slider.setTracking(factory.auto_set)
        slider.setMinimum(0)
        slider.setMaximum(10000)
        slider.setPageStep(1000)
        slider.setSingleStep(100)
        slider.setLow(self._convert_to_slider(self.low))
        slider.setHigh(self._convert_to_slider(self.high))

        QtCore.QObject.connect(slider, QtCore.SIGNAL('sliderMoved(int)'),
                self.update_object_on_scroll)
        panel.addWidget(slider)

        self._label_hi = QtGui.QLineEdit(self.format % self.high)
        QtCore.QObject.connect(self._label_hi, QtCore.SIGNAL('editingFinished()'),
                self.update_high_on_enter)
        panel.addWidget(self._label_hi)

        # The default size is a bit too big and probably doesn't need to grow.
        sh = self._label_hi.sizeHint()
        sh.setWidth(sh.width() / 2)
        self._label_hi.setMaximumSize(sh)

        self.set_tooltip(slider)
        self.set_tooltip(self._label_lo)
        self.set_tooltip(self._label_hi)

    def update_low_on_enter(self):
        try:
            try:
                low = eval(unicode(self._label_lo.text()).strip())
                if self.evaluate is not None:
                    low = self.evaluate(low)
            except Exception, ex:
                low = self.low
                self._label_lo.setText(self.format % self.low)

            if not self.factory.is_float:
                low = int(low)

            if low > self.high:
                low = self.high - self._step_size()
                self._label_lo.setText(self.format % low)

            self.control.slider.setLow(self._convert_to_slider(low))
            self.low = low
        except:
            pass

    def update_high_on_enter(self):
        try:
            try:
                high = eval(unicode(self._label_hi.text()).strip())
                if self.evaluate is not None:
                    high = self.evaluate(high)
            except:
                high = self.high
                self._label_hi.setText(self.format % self.high)

            if not self.factory.is_float:
                high = int(high)

            if high < self.low:
                high = self.low + self._step_size()
                self._label_hi.setText(self.format % high)

            self.control.slider.setHigh(self._convert_to_slider(high))
            self.high = high
        except:
            pass

    def update_object_on_scroll(self, pos):
        low = self._convert_from_slider(self.control.slider.low())
        high = self._convert_from_slider(self.control.slider.high())

        if self.factory.is_float:
            self.low = low
            self.high = high
        else:
            self.low = int(low)
            self.high = int(high)

            # update the sliders to the int values or the sliders
            # will jiggle
            self.control.slider.setLow(self._convert_to_slider(low))
            self.control.slider.setHigh(self._convert_to_slider(high))


    def update_editor(self):
        return

    def _check_max_and_min(self):
        # check if max & min have been defined:
        if self.max is None:
            self.max = self.high
        if self.min is None:
            self.min = self.low

    def _step_size(self):
        slider_delta = self.control.slider.maximum() - self.control.slider.minimum()
        range_delta = self.max - self.min

        return float(range_delta) / slider_delta

    def _convert_from_slider(self, slider_val):
        self._check_max_and_min()
        return self.min + slider_val * self._step_size()

    def _convert_to_slider(self, value):
        self._check_max_and_min()
        return self.control.slider.minimum() + (value - self.min) / self._step_size()

    def _low_changed(self, low):
        if self.control is None:
            return
        if self._label_lo is not None:
            self._label_lo.setText(self.format % low)
        self.control.slider.setLow(self._convert_to_slider(low))

    def _high_changed(self, high):
        if self.control is None:
            return
        if self._label_hi is not None:
            self._label_hi.setText(self.format % high)
        self.control.slider.setHigh(self._convert_to_slider(self.high))

#    def _min_changed(self, min):
#        if self.control is None:
#            return
#        self.control.slider.setMinimum(min)



class BoundsEditor(RangeEditor):

    #TODO why use Trait?
    min = Trait(None, Float)
    max = Trait(None, Float)

#    #TODO min_name, max_name
#    max_name = Str
#    min_name = Str

    def _get_simple_editor_class(self):
        return _BoundsEditor
    def _get_custom_editor_class(self):
        return _BoundsEditor


if __name__ == '__main__':
    from enthought.traits.api import HasTraits, Range, Int, Button, Float
    from enthought.traits.ui.api import View, Item
    #from enthought.traits.ui.qt4.extra.bounds_editor import BoundsEditor
    from bounds_editor import BoundsEditor
    
    class Foo(HasTraits):
        bounds = Range('min',20,value=15)
        
        min = Float
        incr_min = Button("incr_min")
        def _incr_min_fired(self):
            self.min += 1

        incr_low = Button("incr_low")
        def _incr_low_fired(self):
            self.first += 1
        
        first = Float(10)
        def _first_changed(self, old, new):
            print "new low:", new
    
        traits_view = View(
            Item('bounds', 
                editor=BoundsEditor(
#                    min_name='min',
                    low_name='first', 
                    high=20
                )
            ),
            Item('incr_low'),
            Item('incr_min'),
            resizable=True,
        )
    
    Foo().configure_traits()

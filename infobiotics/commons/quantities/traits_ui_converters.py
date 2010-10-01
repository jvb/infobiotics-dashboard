from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Array, Instance, on_trait_change, Trait
from quantities import Quantity
from enthought.traits.ui.api import EnumEditor, View, Item
from infobiotics.commons.traits.ui.values_for_enum_editor import values_for_EnumEditor
from volume import *
from infobiotics.commons.quantities.time import * # avoids clash with compiled module 'time'
from concentration import *

class Converter(HasTraits):

    data = Array
    
    _data_quantity = Instance(Quantity)

    def _data_units_default(self):
        raise NotImplementedError
    
    def _display_units_default(self):
        raise NotImplementedError

    units_editor = Instance(EnumEditor) 

    @on_trait_change('data, data_units')
    def update_data_quantity(self):
        self._data_quantity = Quantity(self.data, self.data_units_)
    
    @on_trait_change('_data_quantity, display_units')
    def print_rescaled__data_quantity(self):
        print self._data_quantity.rescale(self.display_units_)

    def traits_view(self):
        return View(
            Item('data_units',
                editor=self.units_editor,
            ),
            Item('display_units',
                editor=self.units_editor,
            ),
        )


liters = 'liters'
milliliters = 'milli%s (10^-3 %s)' % (liters, liters)
microliters = 'micro%s (10^-6 %s)' % (liters, liters)
nanoliters = 'nano%s (10^-9 %s)' % (liters, liters)
picoliters = 'pico%s (10^-12 %s)' % (liters, liters)
femtoliters = 'femto%s (10^-15 %s)' % (liters, liters)
attoliters = 'atto%s (10^-18 %s)' % (liters, liters)

volume_units = {
    liters:liter,
    milliliters:milliliter,
    microliters:microliter,
    nanoliters:nanoliter,
    picoliters:picoliter,
    femtoliters:femtoliter,
    attoliters:attoliter,
}

VolumeUnit = Trait(milliliters, volume_units)

volume_units_editor = EnumEditor(
    values=values_for_EnumEditor((liters, milliliters, microliters, nanoliters, picoliters, femtoliters, attoliters)),
)

class VolumeConverter(Converter):
    data_units = VolumeUnit
    display_units = VolumeUnit
    units_editor = volume_units_editor


time_units = {
    'years':year,
    'months':month,
    'weeks':week,
    'days':day,
    'hours':hour,
    'minutes':minute,
    'seconds':second,
    'milliseconds':millisecond,
    'microseconds':microsecond,
    'nanoseconds':nanosecond,
    'picoseconds':picosecond,
    'femtoseconds':femtosecond,
    'attoseconds':attosecond,
}

TimeUnit = Trait('seconds', time_units)

time_units_editor = EnumEditor(
    values=values_for_EnumEditor(('years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds', 'milliseconds', 'microseconds', 'nanoseconds', 'picoseconds', 'femtoseconds', 'attoseconds')),
)

class TimeConverter(Converter):
    data_units = TimeUnit
    display_units = TimeUnit
    units_editor = time_units_editor


concentration_units = {
    'molar':molar,
    'millimolar':millimolar,
    'micromolar':micromolar,
    'nanomolar':nanomolar,
    'picomolar':picomolar,
    'femtomolar':femtomolar,
    'attomolar':attomolar,
}

ConcentrationUnit = Trait('molar', concentration_units)

concentration_units_editor = EnumEditor(
    values=values_for_EnumEditor(('molar', 'millimolar', 'micromolar', 'nanomolar', 'picomolar', 'femtomolar', 'attomolar')),
)

class ConcentrationConverter(Converter):
    data_units = ConcentrationUnit
    display_units = ConcentrationUnit
    units_editor = concentration_units_editor


if __name__ == '__main__':
    import numpy as np
#    VolumeConverter(data=np.arange(100)).configure_traits()
#    TimeConverter(data=np.arange(0, 84601, 1)).configure_traits()
    ConcentrationConverter(data=np.arange(100)).configure_traits()

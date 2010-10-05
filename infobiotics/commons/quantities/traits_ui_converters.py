from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Array, Instance, on_trait_change, Trait
from quantities.quantity import Quantity
from enthought.traits.ui.api import EnumEditor, View, Item
from infobiotics.commons.traits.ui.values_for_enum_editor import values_for_EnumEditor
from units.volume import volume_units
from units.time import time_units # avoids clash with compiled module 'time'
from units.concentration import concentration_units
from units.substance import substance_units

class Converter(HasTraits):

    data = Array
    
    _data_quantity = Instance(Quantity)
    
    display_quantity = Instance(Quantity)

    def _data_units_default(self):
        raise NotImplementedError
    
    def _display_units_default(self):
        raise NotImplementedError

    units_editor = Instance(EnumEditor) 

    @on_trait_change('data, data_units')
    def update_data_quantity(self):
        self._data_quantity = Quantity(self.data, self.data_units_)
    
    @on_trait_change('_data_quantity, display_units')
    def update_display_quantity(self):
        self.display_quantity = self._data_quantity.rescale(self.display_units_)

#    @on_trait_change('display_quantity')
#    def print_display_quantity(self):
#        print self.display_quantity

    def traits_view(self):
        return View(
            Item('data_units',
                editor=self.units_editor,
            ),
            Item('display_units',
                editor=self.units_editor,
            ),
        )


TimeUnit = Trait('seconds', time_units)

time_units_editor = EnumEditor(
    values=values_for_EnumEditor(('years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds', 'milliseconds', 'microseconds', 'nanoseconds', 'picoseconds', 'femtoseconds', 'attoseconds')),
)

class TimeConverter(Converter):
    data_units = TimeUnit
    display_units = TimeUnit
    units_editor = time_units_editor


VolumeUnit = Trait('millilitres', volume_units)

volume_units_editor = EnumEditor(
    values=values_for_EnumEditor(('litres', 'milliliters', 'microlitres', 'nanoliters', 'picolitres', 'femtolitres', 'attolitres')),
)

class VolumeConverter(Converter):
    data_units = VolumeUnit
    display_units = VolumeUnit
    units_editor = volume_units_editor


SubstanceUnit = Trait('molecules', substance_units)

substance_units_editor = EnumEditor(
    values=values_for_EnumEditor(('molecules', 'moles', 'millimoles', 'micromoles', 'nanomoles', 'picomoles', 'femtomoles', 'attomoles')),
)

class SubstanceConverter(Converter):
    data_units = SubstanceUnit
    display_units = SubstanceUnit
    units_editor = substance_units_editor


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
#    TimeConverter(data=np.arange(0, 84601, 1)).configure_traits()
#    VolumeConverter(data=np.arange(100)).configure_traits()
    SubstanceConverter(data=np.arange(100)).configure_traits()
#    ConcentrationConverter(data=np.arange(100)).configure_traits()

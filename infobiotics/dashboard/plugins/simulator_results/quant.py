import numpy as np

#molecules = np.arange(1000 * 1000).reshape((100, 100, 100)) # pretend amounts that might come from an mcss simulation
#moles = molecules / N_A * mole # convert molecules to moles by dividing the number of molecules by Avogadro's constant
#molecules = np.array(moles * N_A, dtype=int) # recover molecules by multiplying the number of moles by Avogadro's constant, as integers without possible float-representation rounding errors 
#concentrations = moles / (volume * volume_unit) # convert moles to concentrations by dividing by volume with units

from quantities import UnitQuantity, liter, milli, micro, nano, pico, femto, atto
milliliter = UnitQuantity('milliliter', liter * milli, symbol='mL')
microliter = UnitQuantity('microliter', liter * micro, symbol='uL')
nanoliter = UnitQuantity('nanoliter', liter * nano, symbol='nL')
picoliter = UnitQuantity('picoliter', liter * pico, symbol='pL')
femtoliter = UnitQuantity('femtoliter', liter * femto, symbol='fL')
attoliter = UnitQuantity('attoliter', liter * atto, symbol='aL')

from quantities import mole
molar = UnitQuantity('molar', mole / liter, symbol='M')
millimolar = UnitQuantity('millimolar', mole / liter * milli, symbol='mM')
micromolar = UnitQuantity('micromolar', mole / liter * micro, symbol='uM')
nanomolar = UnitQuantity('nanomolar', mole / liter * nano, symbol='nM')
picomolar = UnitQuantity('picomolar', mole / liter * pico, symbol='pM')
femtomolar = UnitQuantity('femtomolar', mole / liter * femto, symbol='fM')
attomolar = UnitQuantity('attomolar', mole / liter * atto, symbol='aM')

from scipy.constants import N_A # Avogadro's constant 6.0221415e+23
def concentration(molecules, volume, volume_unit, concentration_units=molar):
    moles = molecules / N_A * mole
    return (moles / (volume * volume_unit)).rescale(concentration_units)
#print concentration(N_A, 1, liter) 
##cell_volume = 0.65 * micro * liter # an example cell volume (0.65 ul) ~ the size of an E.coli (Wikipedia: Bacterial_cell_structure)
#print concentration(np.arange(1, 1000 * 1000 + 1, 1000), 0.65, microliter, picomolar) 
#exit()


from quantities import picosecond, nanosecond, microsecond, millisecond, second, minute, hour, day, week, month, year


from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import *
from enthought.traits.ui.api import *
from infobiotics.commons.traits.ui.values_for_enum_editor import values_for_EnumEditor
from quantities import Quantity

class Converter(HasTraits):

    data = Array
    
    _data_quantity = Instance(Quantity)

    data_units = Any
    def _data_units_default(self):
        raise NotImplementedError
    
    display_units = Any
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
    'picoseconds':picosecond,
    'nanoseconds':nanosecond,
    'microseconds':microsecond,
    'milliseconds':millisecond,
    'seconds':second,
    'minutes':minute,
    'hours':hour,
    'days':day,
    'weeks':week,
    'years':year,
}

TimeUnit = Trait('seconds', time_units)

time_units_editor = EnumEditor(
    values=values_for_EnumEditor(('picoseconds', 'nanoseconds', 'microseconds', 'milliseconds', 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years')),
)

class TimeConverter(Converter):
    data_units = TimeUnit
    display_units = TimeUnit
    units_editor = time_units_editor


#mu, sigma = 100, 10 # mean and standard deviation
#s = np.random.normal(mu, sigma, 1000)
#import matplotlib.pyplot as plt
#count, bins, ignored = plt.hist(s, 30, normed=True)
#plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) * 
#               np.exp(-(bins - mu) ** 2 / (2 * sigma ** 2)),
#         linewidth=2, color='r')
#plt.show()
#exit()


if __name__ == '__main__':
    VolumeConverter(data=np.arange(100)).configure_traits()
#    TimeConverter(data=np.arange(0, 84601, 1)).configure_traits()

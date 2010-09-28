import quantities as pq

import numpy as np

time = np.linspace(0, 60, 7) * pq.sec
print time
time.units = pq.min
print time

time_in_minutes = time.rescale('minutes')
print time_in_minutes


molecules = 100
print molecules

volume = 1 * pq.liter * pq.milli
print volume

concentration = molecules / volume 
print concentration

print dir(pq)

concentration = 10 * pq.micro * pq.mole / pq.liter
print concentration

molecules = volume * concentration
print molecules


microliter = pq.liter * pq.micro
nanoliter = pq.liter * pq.nano
attoliter = pq.liter * pq.nano
picoliter = pq.liter * pq.pico
femtoliter = pq.liter * pq.femto

from enthought.traits.api import *
from enthought.traits.ui.api import *

volume_units = {
    'liters':pq.liter,
    'milliliters (10^-3 liters)':pq.milliliter,
    'microliters (10^-6 liters)':microliter,
    'nanoliters (10^-9 liters)':nanoliter,
    'attoliters (10^-10 liters)':attoliter,
    'picoliters (10^-12 liters)':picoliter,
    'femtoliters (10^-15 liters)':femtoliter,
}

volume_units_editor = EnumEditor(
    values={
        'liters':'1:liters',
        'milliliters (10^-3 liters)':'2:milliliters (10^-3 liters)',
        'microliters (10^-6 liters)':'3:microliters (10^-6 liters)',
        'nanoliters (10^-9 liters)':'4:nanoliters (10^-9 liters)',
        'attoliters (10^-10 liters)':'5:attoliters (10^-10 liters)',
        'picoliters (10^-12 liters)':'6:picoliters (1e-12 liters)',
        'femtoliters (10^-15 liters)':'7:femtoliters (1e-15 liters)',
    }
)

class Test(HasTraits):
    
    data = Array
    
    data_quantity = Instance(pq.Quantity)
    
    data_volume_units = Trait(
        'milliliters (10^-3 liters)',
        volume_units
    )
    
    def _data_changed(self):
        self._data_volume_units_changed()
    
    def _data_volume_units_changed(self):
        self.data_quantity = pq.Quantity(self.data, self.data_volume_units_)
    
    display_volume_units = Trait(
        'milliliters (10^-3 liters)',
        volume_units
    )

    def _display_volume_units_changed(self):
        print self.display_volume_units, self.display_volume_units_
        self.data_quantity.units = self.display_volume_units_
        print self.data_quantity 

    view = View(
        Item('data_volume_units',
            editor=volume_units_editor,
        ),
        Item('display_volume_units',
            editor=volume_units_editor,
        ),
    )


if __name__ == '__main__':
    Test(data=np.arange(100)).configure_traits()


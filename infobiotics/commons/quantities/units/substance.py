from quantities.unitquantity import UnitQuantity
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto
from scipy.constants import N_A # Avogadro's constant 6.0221415e+23

mmoles = millimoles = millimole = UnitQuantity('millimoles', milli * mole)
umoles = micromoles = micromole = UnitQuantity('micromoles', micro * mole)
nmoles = nanomoles = nanomole = UnitQuantity('nanomoles', nano * mole)
pmoles = picomoles = picomole = UnitQuantity('picomoles', pico * mole)
fmoles = femtomoles = femtomole = UnitQuantity('femtomoles', femto * mole)
amoles = attomoles = attomole = UnitQuantity('attomoles', atto * mole)
molecules = molecule = UnitQuantity('molecule', (1 / N_A) * mole, symbol='molecules')

substance_units = {
    'moles':mole,
    'millimoles':millimole,
    'micromoles':micromole,
    'nanomoles':nanomole,
    'picomoles':picomole,
    'femtomoles':femtomole,
    'attomoles':attomole,
    
    'molecules':molecule,
    
    'mole':mole,
    'millimole':millimole,
    'micromole':micromole,
    'nanomole':nanomole,
    'picomole':picomole,
    'femtomole':femtomole,
    'attomole':attomole,
}

from quantities.quantity import Quantity

def convert_substance(substance, to_units, from_units=molecule):
    if not isinstance(substance, Quantity):
        if not isinstance(from_units, Quantity):
            from_units = substance_units[from_units] # assumes from_units is a mappable string
        substance = Quantity(substance, from_units)
    if not isinstance(to_units, Quantity):
        to_units = substance_units[to_units] # assumes to_units is a mappable string
    return substance.rescale(to_units)
    
if __name__ == '__main__':
    print convert_substance(100 * millimole, mole)

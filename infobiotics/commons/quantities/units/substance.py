from quantities.unitquantity import UnitQuantity
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto
from scipy.constants import N_A # Avogadro's constant 6.0221415e+23

millimoles = millimole = UnitQuantity('millimoles', milli * mole)#, symbol='mM')
micromoles = micromole = UnitQuantity('micromoles', micro * mole)#, symbol='uM')
nanomoles = nanomole = UnitQuantity('nanomoles', nano * mole)#, symbol='nM')
picomoles = picomole = UnitQuantity('picomoles', pico * mole)#, symbol='pM')
femtomoles = femtomole = UnitQuantity('femtomoles', femto * mole)#, symbol='fM')
attomoles = attomole = UnitQuantity('attomoles', atto * mole)#, symbol='aM')
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

from quantities.unitquantity import UnitQuantity
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto
from scipy.constants import N_A # Avogadro's constant 6.0221415e+23

molecule = UnitQuantity('molecule', (1 / N_A) * mole, symbol='molecules')

millimole = UnitQuantity('millimoles', mole * milli)#, symbol='mM')
micromole = UnitQuantity('micromoles', mole * micro)#, symbol='uM')
nanomole = UnitQuantity('nanomoles', mole * nano)#, symbol='nM')
picomole = UnitQuantity('picomoles', mole * pico)#, symbol='pM')
femtomole = UnitQuantity('femtomoles', mole * femto)#, symbol='fM')
attomole = UnitQuantity('attomoles', mole * atto)#, symbol='aM')

moles_units = {
    'molecules':molecule,
    'moles':mole,
    'millimoles':millimole,
    'micromoles':micromole,
    'nanomoles':nanomole,
    'picomoles':picomole,
    'femtomoles':femtomole,
    'attomoles':attomole,
}

from quantities import Quantity

def convert_substance(substance, out_units, in_units=liters):
    if hasattr(substance, 'units'):
        return convert_substance_with_units(substance, out_units)
    if not isinstance(in_units, Quantity):
        in_units = volume_units[in_units] # assumes in_units is a mappable string
    return convert_volume_with_units(Quantity(volume, in_units), out_units)
    
def convert_volume_with_units(volume, out_units):
    if not isinstance(out_units, Quantity):
        out_units = volume_units[out_units] # assumes out_units is a mappable string
    return volume.rescale(out_units)
    
print convert_volume(100, 'molecules', mole)

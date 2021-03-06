__all__ = [
    'M', 'molar',
    'mM', 'millimolar',
    'uM', 'micromolar',
    'nM', 'nanomolar',
    'pM', 'picomolar',
    'fM', 'femtomolar',
    'aM', 'attomolar',
    'concentration_units',
]

from quantities.unitquantity import UnitQuantity
from quantities.units.volume import liter
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto

M = molar = UnitQuantity('molar', mole / liter, symbol='M')
mM = millimolar = UnitQuantity('millimolar', (milli * mole) / liter , symbol='mM')
uM = micromolar = UnitQuantity('micromolar', (micro * mole) / liter, symbol='uM')
nM = nanomolar = UnitQuantity('nanomolar', (nano * mole) / liter, symbol='nM')
pM = picomolar = UnitQuantity('picomolar', (pico * mole) / liter, symbol='pM')
fM = femtomolar = UnitQuantity('femtomolar', (femto * mole) / liter, symbol='fM')
aM = attomolar = UnitQuantity('attomolar', (atto * mole) / liter, symbol='aM')

concentration_units = {
    'molar':molar,
    'millimolar':millimolar,
    'micromolar':micromolar,
    'nanomolar':nanomolar,
    'picomolar':picomolar,
    'femtomolar':femtomolar,
    'attomolar':attomolar,
}

##def concentration(molecules, volume, volume_units, concentration_units=molar):
##    return (moles(molecules) / (volume * volume_units)).rescale(concentration_units)
#
#def concentration(moles, volume, volume_units, concentration_units=molar):
#    return (moles / (volume * volume_units)).rescale(concentration_units)
#

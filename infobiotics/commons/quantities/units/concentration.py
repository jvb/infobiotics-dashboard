from quantities.unitquantity import UnitQuantity
from quantities.units.volume import liter
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto

molar = UnitQuantity('molar', mole / liter, symbol='M')
millimolar = UnitQuantity('millimolar', (milli * mole) / liter , symbol='mM')
micromolar = UnitQuantity('micromolar', (micro * mole) / liter, symbol='uM')
nanomolar = UnitQuantity('nanomolar', (nano * mole) / liter, symbol='nM')
picomolar = UnitQuantity('picomolar', (pico * mole) / liter, symbol='pM')
femtomolar = UnitQuantity('femtomolar', (femto * mole) / liter, symbol='fM')
attomolar = UnitQuantity('attomolar', (atto * mole) / liter, symbol='aM')

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

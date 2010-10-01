from quantities.unitquantity import UnitQuantity
from quantities.units.volume import liter
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto
from scipy.constants import N_A # Avogadro's constant 6.0221415e+23

molar = UnitQuantity('molar', mole / liter, symbol='M')
millimolar = UnitQuantity('millimolar', mole / liter * milli, symbol='mM')
micromolar = UnitQuantity('micromolar', mole / liter * micro, symbol='uM')
nanomolar = UnitQuantity('nanomolar', mole / liter * nano, symbol='nM')
picomolar = UnitQuantity('picomolar', mole / liter * pico, symbol='pM')
femtomolar = UnitQuantity('femtomolar', mole / liter * femto, symbol='fM')
attomolar = UnitQuantity('attomolar', mole / liter * atto, symbol='aM')

concentration_units = {
    'molar':molar,
    'millimolar':millimolar,
    'micromolar':micromolar,
    'nanomolar':nanomolar,
    'picomolar':picomolar,
    'femtomolar':femtomolar,
    'attomolar':attomolar,
}

def concentration(molecules, volume, volume_units, concentration_units=molar):
    moles = molecules / N_A * mole
    return (moles / (volume * volume_units)).rescale(concentration_units)

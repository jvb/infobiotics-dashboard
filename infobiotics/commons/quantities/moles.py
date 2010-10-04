from quantities.unitquantity import UnitQuantity
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto
#from scipy.constants import N_A # Avogadro's constant 6.0221415e+23

moles = mole
millimoles = UnitQuantity('millimoles', mole * milli)#, symbol='mM')
micromoles = UnitQuantity('micromoles', mole * micro)#, symbol='uM')
nanomoles = UnitQuantity('nanomoles', mole * nano)#, symbol='nM')
picomoles = UnitQuantity('picomoles', mole * pico)#, symbol='pM')
femtomoles = UnitQuantity('femtomoles', mole * femto)#, symbol='fM')
attomoles = UnitQuantity('attomoles', mole * atto)#, symbol='aM')

moles_units = {
    'moles':moles,
    'millimoles':millimoles,
    'micromoles':micromoles,
    'nanomoles':nanomoles,
    'picomoles':picomoles,
    'femtomoles':femtomoles,
    'attomoles':attomoles,
}

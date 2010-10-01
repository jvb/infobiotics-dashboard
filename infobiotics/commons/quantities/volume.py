from quantities.unitquantity import UnitQuantity
from quantities.units.volume import liter
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto

milliliter = UnitQuantity('milliliter', liter * milli, symbol='mL')
microliter = UnitQuantity('microliter', liter * micro, symbol='uL')
nanoliter = UnitQuantity('nanoliter', liter * nano, symbol='nL')
picoliter = UnitQuantity('picoliter', liter * pico, symbol='pL')
femtoliter = UnitQuantity('femtoliter', liter * femto, symbol='fL')
attoliter = UnitQuantity('attoliter', liter * atto, symbol='aL')

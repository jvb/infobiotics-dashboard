from quantities.unitquantity import UnitQuantity
from quantities.units.volume import liter
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto

milliliter = UnitQuantity('milliliter', liter * milli, symbol='mL')
microliter = UnitQuantity('microliter', liter * micro, symbol='uL')
nanoliter = UnitQuantity('nanoliter', liter * nano, symbol='nL')
picoliter = UnitQuantity('picoliter', liter * pico, symbol='pL')
femtoliter = UnitQuantity('femtoliter', liter * femto, symbol='fL')
attoliter = UnitQuantity('attoliter', liter * atto, symbol='aL')

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

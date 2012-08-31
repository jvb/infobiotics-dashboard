__all__ = [ #TODO add convert_volume function?
    'l', 'L', 'litre', 'liter',
    'ml', 'mL', 'millilitre', 'milliliter',
    'ul', 'uL', 'microlitre', 'microliter',
    'nl', 'nL', 'nanolitre', 'nanoliter',
    'pl', 'pL', 'picolitre', 'picoliter',
    'fl', 'fL', 'femtolitre', 'femtoliter',
    'al', 'aL', 'attolitre', 'attoliter',
    'volume_units',
]

from quantities.unitquantity import UnitQuantity
from quantities.units.volume import liter
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto

l = L = litre = liter
ml = mL = millilitre = milliliter = UnitQuantity('milliliter', milli * liter, symbol='mL')
ul = uL = microlitre = microliter = UnitQuantity('microliter', micro * liter, symbol='uL')
nl = nL = nanolitre = nanoliter = UnitQuantity('nanoliter', nano * liter, symbol='nL')
pl = pL = picolitre = picoliter = UnitQuantity('picoliter', pico * liter, symbol='pL')
fl = fL = femtolitre = femtoliter = UnitQuantity('femtoliter', femto * liter, symbol='fL')
al = aL = attolitre = attoliter = UnitQuantity('attoliter', atto * liter, symbol='aL')

volume_units = {
    # US English
    'liters':liter,
    'milliliters':milliliter,
    'microliters':microliter,
    'nanoliters':nanoliter,
    'picoliters':picoliter,
    'femtoliters':femtoliter,
    'attoliters':attoliter,
    # UK English
    'litres':liter,
    'millilitres':milliliter,
    'microlitres':microliter,
    'nanolitres':nanoliter,
    'picolitres':picoliter,
    'femtolitres':femtoliter,
    'attolitres':attoliter,
    
}

#from quantities import Quantity
#
#def convert_volume(volume, out_units, in_units=liters):
#    if hasattr(volume, 'units'):
#        return convert_volume_with_units(volume, out_units)
#    if not isinstance(in_units, Quantity):
#        in_units = volume_units[in_units] # assumes in_units is a mappable string
#    return convert_volume_with_units(Quantity(volume, in_units), out_units)
#    
#def convert_volume_with_units(volume, out_units):
#    if not isinstance(out_units, Quantity):
#        out_units = volume_units[out_units] # assumes out_units is a mappable string
#    return volume.rescale(out_units)
#    
#print convert_volume(100, 'millilitres', 'nanolitres')


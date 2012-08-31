__all__ = [
    'centimeter', 'meter', 'millimeter', 'micrometer', 'nanometer', 'picometer', 'attometer',
    'centimetre', 'metre', 'millimetre', 'micrometre', 'nanometre', 'picometre', 'attometre',
    'm'
]
from quantities.unitquantity import UnitQuantity
from quantities.units.prefixes import atto
from quantities.units import (
    centimeter, meter, millimeter, micrometer, nanometer, picometer,
    centimetre, metre, millimetre, micrometre, nanometre, picometre,
)

m = meter

am = attometer = attometre = UnitQuantity('attometre', atto * meter)


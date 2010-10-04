from quantities.unitquantity import UnitQuantity
from quantities.units.volume import liter
from quantities.units.substance import mole
from quantities.units.prefixes import milli, micro, nano, pico, femto, atto
from scipy.constants import N_A # Avogadro's constant 6.0221415e+23
from moles import moles

molar = UnitQuantity('molar', mole / liter, symbol='M')
millimolar = UnitQuantity('millimolar', mole * milli / liter , symbol='mM')
micromolar = UnitQuantity('micromolar', mole * micro / liter, symbol='uM')
nanomolar = UnitQuantity('nanomolar', mole * nano / liter, symbol='nM')
picomolar = UnitQuantity('picomolar', mole * pico / liter, symbol='pM')
femtomolar = UnitQuantity('femtomolar', mole * femto / liter, symbol='fM')
attomolar = UnitQuantity('attomolar', mole * atto / liter, symbol='aM')

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
if __name__ == '__main__':
    
    import numpy as np
    from volume import microliter
    from quantities import Quantity
    from quantities.units.substance import mole
#    print concentration(np.arange(0, 1, 0.1), 10, microliter, nanomolar)
#    print concentration(Quantity(np.arange(0, 1, 0.1), mole), 10, microliter, nanomolar)
    
    #def moles(molecules):#, moles_units=moles):
    #    return molecules / N_A * mole
    #
#    #from quantities.unitquantity import dimensionless
#    ##molecule = mole / N_A
    
    molecule = UnitQuantity('molecule', (1 / N_A) * mole, symbol='molecules')
    print (1 * mole).rescale(molecule)
    print 100 * molecule
    
#    
#    #from moles import moles
#    #
#    #def molecules(moles, moles_units=moles):
#    #    return (N_A * moles * moles_units) * molecule
#    #
#    #print molecules(1)#, moles(1 * N_A)

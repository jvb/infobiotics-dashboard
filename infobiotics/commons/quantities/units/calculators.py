from __future__ import division
from infobiotics.commons.quantities.api import *
from quantities import UnitTime

#def concentration(moles=1 * mole, volume=1 * litre, concentration_unit=molar):
#    return (moles / volume).rescale(concentration_unit)
#print concentration()
#print concentration(100 * molecule, 1 * microlitre)
#print 
#
#def substance(concentration=1 * molar, volume=1 * litre, substance_unit=mole):
#    return (volume * concentration).rescale(substance_unit)
#print substance()
#print substance(concentration=1 * micromolar, volume=1 * microlitre)
#print 
#
#def molecules(concentration=1 * molar, volume=1 * litre):
#    return substance(concentration, volume, substance_unit=molecule)
#print molecules()
#print molecules(concentration=1 * micromolar, volume=1 * microlitre)
#print 
#
#def substance_per_time(concentration_per_time=1 * molar / second, volume=1 * litre, substance_unit=mole, time_unit=second):
#    return (volume * concentration_per_time).rescale(substance_unit / time_unit)
#print substance_per_time()
#print substance_per_time(concentration_per_time=1 * micromolar / hour, volume=1 * microlitre,)
#print 

cell_volume = 1 * (micro * metre) ** 3 # == 1 * femtolitre != 1 * microlitre
default_time_unit = hour

'''
0th order: c=NVk (k has units M.s-1)
1st order: c=k (k has units s-1)
2nd order (same reactants i.e. X + X -> ...): c=2k/(NV) (k has units M-1.s-1)
2nd order (different reactants i.e. X + Y -> ...): c=k/(NV) (k has units M-1.s-1)
where:
c is the stochastic rate constant (units s-1)
k is the deterministic rate constant
N is Avogadro's number (units mol-1)
V is the compartment volume (units m3).
'''

V = cell_volume.rescale(metre ** 3)
#print 'V', V
N = N_A * (mole ** -1)
#print 'N', N

def zeroth(k, time_unit=default_time_unit):
    ''' k has units molarity * time ** -1 '''
    return (N * V * k.rescale(molar / second)).rescale(time_unit ** -1)

def first(k, time_unit=default_time_unit):
    ''' k has units time ** -1 '''
    return k.rescale(time_unit ** -1)

def second_homo(k, time_unit=default_time_unit):
    ''' k has units molarity**-1 time**-1 '''
    return ((2 * k.rescale(molar ** -1 * second ** -1)) / (N * V)).rescale(time_unit ** -1)

def second_hetero(k, time_unit=default_time_unit):
    ''' k has units molarity**-1 time**-1 '''
    return (k.rescale(molar ** -1 * second ** -1) / (N * V)).rescale(time_unit ** -1)

k_on = 2 * 10 ** 6 * M ** -1 * s ** -1
c_on = second_hetero(k_on)
def dissociation(K_D):
    k_off = K_D * k_on
    return 'c_off = %s' % first(k_off)
    
def conversion_function_from_units(q):
    ''' *Cannot* distinguish between hetero and homo second order reactions and
    assumes hetero. For homo multiply c by 2. '''
    if not hasattr(q, 'dimensionality'):
        return lambda _: q
    molarity = 0
    time = 0
    for key, value in q.dimensionality.iteritems():
        if type(key) == UnitQuantity:
            molarity = value
        elif type(key) == UnitTime:
            time = value
    if molarity > 0 and time < 0:
        return zeroth
    elif molarity == 0 and time < 0:
        return first
    elif molarity < 0 and time < 0:
        return second_hetero
    elif molarity > 0 and time == 0:
        return dissociation 


if __name__ == '__main__':
    
    from infobiotics.commons.ordereddict import OrderedDict
    parameters = OrderedDict([
        ('g_S0', 0.1 * micromolar / hour),
        ('g_SA', 1.0 * micromolar / hour),
        ('h_A', 2),
        ('K_SA', 0.2 * micromolar),
        ('k_+S', 100 / hour),
        ('h_Q', 2),
        ('K_S', 0.008 * micromolar),
        ('K_+p', 250 / micromolar / hour),
        ('k_-p', 200 / micromolar / hour),
        ('k_D', 90 / hour),
        ('m_s', 1.5 / hour),
        ('g_A', 10 / hour),
        ('m_A', 1 / hour),
        ('K_XI', .005 * micromolar),
        ('K_ZI', .005 * micromolar),
        ('h_I', 2),
        ('g_X0', 0 * micromolar / hour),
        ('g_Z0', 0 * micromolar / hour),
        ('K_XA', 0.1 * micromolar),
        ('K_ZA', 0.2 * micromolar),
        ('h_A', 2),
        ('g_XA', 3.33 * micromolar / hour),
        ('g_ZA', 1.67 * micromolar / hour),
        ('k_+RX', 14 / micromolar / hour),
        ('k_-RX', 1 / hour),
        ('k_+EX', 17 / micromolar / hour),
        ('k_-EX', 1 / hour),
        ('k_+RZ', 14 / micromolar / hour),
        ('k_-RZ', 1 / hour),
        ('k_+EZ', 20 / micromolar / hour),
        ('k_-EZ', 1 / hour),
        ('n', 4),
        ('m_X', 15 / hour),
        ('m_Z', 7 / hour),
        ('g_R', 0.3 * micromolar / hour),
        ('m_R', 1 / hour),
        ('g_E', 12 * micromolar / hour),
        ('K_ER', 0.2 * micromolar),
        ('K_EE', 0.2 * micromolar),
        ('m_E', 1 / hour),
        ('m_RX', 1.5 / hour),
        ('m_EX', 1.5 / hour),
        ('m_RZ', 1.5 / hour),
        ('m_EZ', 1.5 / hour),
        ('g_I', 0.5 * micromolar / hour),
        ('K_IR', 0.005 * micromolar),
        ('K_IE', 0.038 * micromolar),
        ('m_I', 3 / hour),
        ('g_Q', 120 * uM / h),
        ('K_QR', 0.04 * micromolar),
        ('K_QE', 0.1 * micromolar),
        ('m_Q', 10 / hour),
        ('m_QE', 10 / hour),
        ('d', 100 / hour),
        ('w', 0.02), #* litre),
        ('m_B', 0.05 / hour),
    ])
                
    print 'parameter'.ljust(10), 'stochastic constant (c)'.rjust(35), 'deterministic constant (k)'.rjust(35)
    for name, k in parameters.iteritems():
        print name.ljust(10), str(conversion_function_from_units(k)(k)).rjust(35), str(k).rjust(35)
    print 'c_on'.ljust(10), str(c_on).rjust(35), str(k_on).rjust(35)

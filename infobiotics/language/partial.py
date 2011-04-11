from functools import partial

def zeroth_or_first(constant):
    return constant
source = partial(zeroth_or_first, 1)
print source()

first = partial(zeroth_or_first, 2)
print first()

class Compartment(object):
    n = [5]

compartment = Compartment()

def second_homo(constant, index, compartment):
    return constant * 0.5 * (compartment.n[index] - 1)
s1 = partial(second_homo, 3, 0, compartment)
print s1()

def second_hetero(constant, index, compartment):
    return constant * compartment.n[index]
s2 = partial(second_hetero, 4, 0, compartment)
print s2() 

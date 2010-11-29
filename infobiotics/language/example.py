from infobiotics.language import *


class bacteria(compartment):

    a = 10
    b = species('b', 0)

    r1 = 'a -> b 0.1'

    r2 = reaction('b 0.2-> a')

    r3 = reaction('b + b -> d 0.2', desc='complexation')



def degradation(species, rate):
    return reaction(reactants_inside=species, rate=rate)

def association(s1, s2, rate):
    return reaction(reactants_inside={s1:1, s2:1}, products_inside={s1.name + '_' + s2.name:1})

def dissociation(s1, s2, rate):
    return reaction(reactants_inside={s1:1, s2:1}, products_inside={s1.name + '_' + s2.name:1})

def complexation(s1, s2, rate_ass, rate_diss):
    return association(s1, s2, rate_ass), dissociation(s1, s2, rate_diss)



b = bacteria(
    degradation('a', 0.1),
    degradation('b', 0.2)
)

print b.str()

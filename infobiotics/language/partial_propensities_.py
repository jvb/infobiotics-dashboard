from multiset import multiset
import math

def id_generator(prefix):
    i = 0
    while True:
        i += 1
        yield '%s%d' % (prefix, i)

reaction_id_generator = id_generator('R')

class reaction(object):
    def __init__(self, reactants={}, products={}, constant=0):
        self.id = reaction_id_generator.next()
        self.reactants = multiset(reactants)
        self.products = multiset(products)
        self.constant = float(constant)
    def __str__(self):
        return '"%s: %s -> %s"' % (self.id, self.reactants, self.products)
    def __repr__(self):
#        return str(self)
        return self.id
    
c1 = 1
c2 = 1
c3 = 1
c4 = 1
c5 = 1

R1 = reaction(('S1', 'S2'), ('S3'), c1)
R2 = reaction((), ('S1'), c2)
R3 = reaction(('S2', 'S2'), ('S1'), c3)
R4 = reaction(('S3',), (), c4)
R5 = reaction(('S1', 'S3'), ('S2'), c5)
#print R5
reactions = [R1, R2, R3, R4, R5]

'''
1. Initialization: set t <- ; initialize n, Pi, Lambda, Sigma; a <- sum(Sigma);
delta_a <- 0; generate L, U1, U2 and U3
'''
t = 0
n = []
Pi = [[], ]
Lambda = []
Sigma = []
a = sum(Sigma)
delta_A = 0
pass
L = [[], ]
U1 = [[], ]
U2 = [[], ]
U3 = [[], ]

'''
2. Sample mu: generate a uniform random number r_1 between 0 and 1 and 
determine the group index I and the element index J according to Eqs. (2), (4),
and (5); mu <- L_IJ
'''
pass

'''
Sample tau: generate a uniform random number r_2 between 0 and 1 and compute
the time to the next reaction tau as tau <- a^-1 * ln(r_2^-1)
'''
pass
tau = a ^ -1 * math.log(r_2 ^ -1)

'''
4. Update n: for each index k of U1_mu, l <- U1_u,k and n_l <- n_l+U2_u,k
'''
pass

'''
5. Update Pi, Lambda, Sigma and compute delta_a, the change in a:
    For each index k of U1_mu, do:
'''
for k, _ in enumerate(U1_mu):
#5.1
    pass
#5.2. For each index m of U3_l, do:
    for m, _ in enumerate(U3_l):
#5.2.1
        pass
#5.2.2
        pass
#5.2.3
        pass
#5.2.4
        pass
#5.2.5
        pass
#5.2.6
        pass
#5.3
    pass

'''
6. Update a and increment time: a <- a + delta_a; delta_a <- 0; t <- t + tau
'''
pass

'''
7. Go to step 2
'''
pass

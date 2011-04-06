from math import log
from random import random
from multiset import multiset
#m = multiset({'S1': 2})
#assert len(m) == 1
#assert m.cardinality() == 2


class reaction(object):
    def __init__(self, reactants={}, products={}, constant=0):
        self.reactants = multiset(reactants)
        self.products = multiset(products)
        self.constant = float(constant)
    def __str__(self):
        return '"%s -> %s"' % (self.reactants, self.products)
    def __repr__(self):
        return str(self)
    

def PDM(reactions, state, t_f):
    '''Initialize compartment where reactions is a list of reaction objects
    and state is a dictionary of species amounts.'''
    
    print
#    print 'reactions ='
    for i, r in enumerate(reactions):
        print 'R_%s =' % i, r
    print
    
    # add missing species to state
    for r in reactions:
        for s in r.reactants.keys() + r.products.keys():
            try:
                _ = state[s]
            except KeyError:
                state[s] = 0

    '''
    1. Initialization: set t <- 0; initialize n, Pi, Lambda, Sigma; a <- sum(Sigma);
    delta_a <- 0; generate L, U1, U2 and U3
    '''
    t = 0

    # initialize n
    species = sorted(state.keys())
    n = [state[s] for s in species]

    U3 = [[] for _ in range(len(species) + 1)]
    Pi = [[] for _ in range(len(species) + 1)]
    L = [[] for _ in range(len(species) + 1)]

    # initialize Pi and L
    for i, r in enumerate(reactions):
        cardinality = r.reactants.cardinality()
        if cardinality == 0:
            Pi[0].append(r.constant)
            L[0].append(i)
            continue
        else:
            reactants = r.reactants.keys()
        if cardinality == 1:
            reactant_index = species.index(reactants[0])
            pi = r.constant
        elif cardinality == 2:
            if len(reactants) == 2:
                # heterogenous
                reactant_indices = [species.index(s) for s in reactants] 
                reactant_index = min(reactant_indices)
                dependant_index = max(reactant_indices)
                pi = r.constant * n[dependant_index]
                
            else:
                # homogenous
                reactant_index = species.index(reactants[0])
                dependant_index = reactant_index
                pi = r.constant * 0.5 * (n[dependant_index] - 1)
        Pi_index = reactant_index + 1 
        Pi[Pi_index].append(pi)
        L[Pi_index].append(i)
        if cardinality == 2: 
            U3[dependant_index + 1].append((Pi_index, len(Pi[Pi_index]) - 1))
    
    # initialize Lambda
    Lambda = [sum(pies) if len(pies) > 0 else 0 for pies in Pi]

    # initialize Sigma
    Sigma = [Lambda[0]]
    for i, n_i in enumerate(n):
        Sigma.append(n_i * Lambda[i + 1])

    assert Lambda[0] == Sigma[0]
    Sigma_0_max = Lambda_0_max = Sigma[0]

    a = sum(Sigma)
    
    delta_a = 0
    
    U1 = [[species.index(s) for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]

    U2 = [[r.products[s] - r.reactants[s] for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]
    
#    print 'L = '
    for i, outer in enumerate(L):
        print 'L_%s' % i,
        for inner in outer:
            print inner,
        print
    print
#    print 'U1 ='
    for i, outer in enumerate(U1):
        print 'U1_%s =' % i,
        for inner in outer:
            print inner,
        print
    print
#    print 'U2 ='
    for i, outer in enumerate(U2):
        print 'U2_%s =' % i,
        for inner in outer:
            print inner,
        print
    print
#    print 'U3 ='
    for i, outer in enumerate(U3):
        print 'U3_%s =' % i,
        if len(outer) == 0:
            print '-',
        for inner in outer:
            print inner,
        print
    print

    reactions_performed = 0
    while a > 0 and t < t_f and reactions_performed < 10:
        
        print '---------------------------------------'
        print
        print 'time %f' % t, n
        print
#        print 'Pi ='
        for i, outer in enumerate(Pi):
            print 'Pi_%s =' % i,
            for inner in outer:
                print inner,
            print
        print
#        print 'Lambda ='
        for i, outer in enumerate(Lambda):
            print 'Lambda_%s =' % i, outer
        print
#        print 'Sigma:'
        for i, outer in enumerate(Sigma):
            print 'Sigma_%s =' % i, outer
        print
        print 'a = %s' % a
        print 'delta_a = %s' % delta_a
        print

        '''
        2. Sample mu: generate a uniform random number r_1 between 0 and 1 and 
        determine the group index I and the element index J according to Eqs. (2), (4),
        and (5); mu <- L_IJ
        '''
        r_1 = random()
        r_1a = r_1 * a
        print 'r_1a = %s' % r_1a,
        cumulative_sum = 0
        print Sigma,
        for i, sigma in enumerate(Sigma):
            I = i
            cumulative_sum += sigma
            if cumulative_sum > r_1a:
                break
        if debug:
            print 'I = %s' % I
        
        Phi = sum(Sigma[:I + 1])
        print 'Phi = %s' % Phi,
        if I > 0: # avoid divide by zero (not mentioned in paper!)
            Psi = (r_1a - Phi + Sigma[I]) / n[I - 1]
        else:
            Psi = (r_1a - Phi + Sigma[I])
        print 'Psi = %s' % Psi, Pi[I],
        cumulative_sum = 0
        for j in range(len(Pi[I])):
            J = j
            cumulative_sum += Pi[I][j]
            if cumulative_sum > Psi:
                break
        if debug:
            print 'J = %s' % J
        
        
        mu = L[I][J]
        print 'mu = %s' % mu, '(%s)' % reactions[mu], I, Sigma[I]
        
        '''
        Sample tau: generate a uniform random number r_2 between 0 and 1 and compute
        the time to the next reaction tau as tau <- a^-1 * ln(r_2^-1)
        '''
        r_2 = random()
        print 'a = %s, r_2=%s' % (a, r_2)
        tau = a ** -1 * log(r_2 ** -1)
        if tau <= 0:
            raise ValueError
#            if debug:
#                print 'tau:', tau
        
        '''
        4. Update n: for each index k of U1_mu, l <- U1_u,k and n_l <- n_l+U2_u,k
        '''
        for k, l in enumerate(U1[mu]):
            print n, '->',
            n[l] += U2[mu][k]
            print n
        # break on negative population
        for n_i in n:
            if n_i < 0:
                raise ValueError
            

        '''
        5. Update Pi, Lambda, Sigma and compute delta_a, the change in a:
            For each index k of U1_mu, do:
        '''
        for k, l in enumerate(U1[mu]): # 5.1
            print 'l = %s' % l, '# index of species in reaction %s' % mu  
            
            # 5.2. For each index m of U3_l, do:
            for i, j in U3[l]: # 5.2.1
                if i == 0:
                    raise ValueError
                
                # skips zeroth and first order reactions because they are not in U3
                print '(i, j) = %s' % ((i, j),), '# major and minor indices of partial propensity in Pi'

                # 5.2.2 and 5.2.3
                delta_Pi_i_j = reactions[mu].constant * U2[mu][k] if l != i else 0.5 * reactions[mu].constant * U2[mu][k] 
                Pi[i][j] += delta_Pi_i_j
                Lambda[i] += delta_Pi_i_j
                
                # 5.2.4
                Sigma_temp = Sigma[i]
                print 'Sigma_temp = %s' % Sigma_temp
                
                # 5.2.5
                Sigma[i] = n[i - 1] * Lambda[i]
                print 'Sigma[i] = %s' % Sigma[i]
                
                # 5.2.6
                delta_a += Sigma[i] - Sigma_temp
                if debug:
                    print 'delta_a = %s' % delta_a
            
            # 5.3
            print 'l = %s' % l
            print 'n[l] = %s' % n[l]
            print 'Lambda[l] = %s' % Lambda[l]
            print 'Sigma[l] = %s' % Sigma[l]
            # fails here with only source reactions because there is no
            # Lambda or Sigma group indexed by l 
            delta_a += n[l] * Lambda[l] - Sigma[l]
            print 'delta_a = %s' % delta_a
            Sigma[l] = n[l] * Lambda[l]
            print 'Sigma[l] = %s' % Sigma[l]
        
        assert Lambda[0] == Lambda_0_max
        assert Sigma[0] == Sigma_0_max
        
        '''
        6. Update a and increment time: 
            a <- a + delta_a; 
            delta_a <- 0; 
            t <- t + tau
        '''
        a += delta_a
        print 'a = %s' % a
        delta_a = 0
        t += tau

        '''
        7. Go to step 2
        '''

        reactions_performed += 1
        print '%d reactions performed' % reactions_performed
            
        
    print '============================'
    print 'time %f' % t, n

def main():
  
    reactions = [
        reaction(['S1', 'S2'], ['S3'], 1),
        reaction([], ['S1'], 1),
        reaction(['S2', 'S2'], ['S1'], 1),
        reaction(['S3'], [], 1),
        reaction(['S1', 'S3'], ['S2'], 1),
    ]
    
    state = {
        'S1':1,
        'S2':1,
        'S3':1,
    }
    
#    reactions = [
#        reaction([], ['a'], 1),
#        reaction(['a'], ['a'], 1),
#        reaction([], ['b'], 1),
#        reaction([], ['c'], 1),
#    ]
    
#    simulation = PDM()
#    simulation.initialize(reactions, state)
#    simulation.run()
    simulation = PDM(reactions, state, t_f=10)

debug = True
if __name__ == '__main__':
    main()
    

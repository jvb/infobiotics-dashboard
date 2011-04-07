from __future__ import division
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
        return '%s -> %s' % (self.reactants, self.products)
    def __repr__(self):
        return str(self)
    

def PDM(reactions, state, t_f):
    '''Initialize compartment where reactions is a list of reaction objects,
    state is a dictionary of species amounts and t_f is the maximum simulated
    time (in whatever units the reactions stochastic rate constants are).'''
    
    for i, r in enumerate(reactions):
        print 'R_%s =' % (i), r
    print
    
    M = len(reactions)
    
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
    N = len(species)
    n = [state[s] for s in species]

    def initialize_Pi_L_U3_Lambda_Sigma():
        U3 = [[] for _ in range(N)]
        Pi = [[] for _ in range(N + 1)]
        L = [[] for _ in range(N + 1)]
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
                U3[dependant_index].append((Pi_index, len(Pi[Pi_index]) - 1))
        
        Lambda = [sum(pies) if len(pies) > 0 else 0 for pies in Pi]

        Sigma = [Lambda[0]]
        for i, n_i in enumerate(n):
            Sigma.append(n_i * Lambda[i + 1])
        
        assert Lambda[0] == Sigma[0]
        
        return Pi, L, U3, Lambda, Sigma
    
    Pi, L, U3, Lambda, Sigma = initialize_Pi_L_U3_Lambda_Sigma()
    
    Sigma_0 = Lambda_0 = Sigma[0]

    def compare_Pi(Pi1=Pi):
        Pi2, L, U3, Lambda, Sigma = initialize_Pi_L_U3_Lambda_Sigma()
        try:
            for i, Pi1_i in enumerate(Pi1):
                for j, Pi1_i_j in enumerate(Pi1_i):
                    assert Pi1_i_j == Pi2[i][j]
        except AssertionError:
            print 'actual:'
            print_Sigma_n_Lambda_Pi(Sigma, Lambda, Pi1)
            print 'correct:'
            print_Sigma_n_Lambda_Pi(Sigma, Lambda, Pi2)
            print 'problem:'
            print i, j, Pi1_i_j, Pi2[i][j]
            
    compare_Pi()
    
    def print_Sigma_n_Lambda_Pi(Sigma=Sigma, Lambda=Lambda, Pi=Pi):
        print 'i  Sigma  <- n    <-   Lambda <- Pi'
        for i in range(len(Pi)):
            Sigma_i = str(Sigma[i]).ljust(10)
            Lambda_i = str(Lambda[i]).ljust(10)
            if i > 0:
                n_i = str(n[i - 1]).ljust(10)
            else:
                n_i = '-'.ljust(10)
            print '%s%s%s%s%s' % (str(i).ljust(3), Sigma_i, n_i, Lambda_i, ', '.join(str(pi) for pi in Pi[i]))
#        print

    def DM_a0():
        a0 = 0
        for r in reactions:
            cardinality = r.reactants.cardinality()
            c = r.constant
            if cardinality == 0:
                a0 += c
                continue
            reactants = r.reactants.keys()
            if cardinality == 1:
                a0 += c * n[species.index(reactants[0])]
            elif cardinality == 2:
                n_i = n[species.index(reactants[0])]
                if len(reactants) == 1:
                    # homo
                    a0 += c * 0.5 * n_i * (n_i - 1)
                else:
                    # hetero
                    a0 += c * n_i * n[species.index(reactants[1])]
        return a0

    a = sum(Sigma)
    
    delta_a = 0
    
    U1 = [[species.index(s) for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]

    U2 = [[r.products[s] - r.reactants[s] for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]
    
    print 'L = look-up table of reaction indicies of partial propensities (Pi)'
    for i, outer in enumerate(L):
        print 'L_%s' % i,
        for inner in outer:
            print inner,
        print
    print
    print 'U1 is an array of M arrays, where the ith array contains the indices of all species involved in the ith reaction'
    for i, outer in enumerate(U1):
        print 'U1_%s =' % i,
        for inner in outer:
            print inner,
        print
    print
    print 'U2 is an array of M arrays contains the corresponding stoichiometry (change in population of each species upon reaction) of the species references by U1'
    for i, outer in enumerate(U2):
        print 'U2_%s =' % i,
        for inner in outer:
            print inner,
        print
    print
    print 'U1 and U2 are sparse representations of the stoichometric matrix'
    print
    print
    print 'U3 is an array of N arrays, where the ith array contains the indices of all entries in Pi that depend on n_i'
    for i, outer in enumerate(U3):
        print 'U3_%s =' % i,
        if len(outer) == 0:
            print '-',
        for inner in outer:
            print inner,
        print
    print
    print 'U3 is the dependency graph over species'
    print
#    print
#    print_Sigma_n_Lambda_Pi()
#    print
    reactions_performed = 0
    while a > 0 and t < t_f:# and reactions_performed < 3:
        print '---------------------------------------'

        print
        print 'time %f' % t
        for i, s in enumerate(species):
            print s, '=', n[i]
        print
##        print 'Pi ='
#        for i, outer in enumerate(Pi):
#            print 'Pi_%s =' % i,
#            for inner in outer:
#                print inner,
#            print
#        print
##        print 'Lambda ='
#        for i, outer in enumerate(Lambda):
#            print 'Lambda_%s =' % i, outer
#        print
##        print 'Sigma:'
#        for i, outer in enumerate(Sigma):
#            print 'Sigma_%s =' % i, outer
#        print
#        print 'a = %s' % a
#        print 'delta_a = %s' % delta_a
#        print

#        print_Sigma_n_Lambda_Pi()

#        exit()

        '''
        2. Sample mu: generate a uniform random number r_1 between 0 and 1 and 
        determine the group index I and the element index J according to Eqs. (2), (4),
        and (5); mu <- L_IJ
        '''
        r_1 = random()
        r_1a = r_1 * a
#        print 'r_1a = %s' % r_1a,
        cumulative_sum = 0
#        print Sigma,
        for i, sigma in enumerate(Sigma):
            I = i
            cumulative_sum += sigma
            if cumulative_sum > r_1a:
                break
#        print 'I = %s' % I
        
        Phi = sum(Sigma[:I + 1])
#        print 'Phi = %s' % Phi,
        if I > 0: # avoid divide by zero (not mentioned in paper!)
            Psi = (r_1a - Phi + Sigma[I]) / n[I - 1]
        else:
            Psi = (r_1a - Phi + Sigma[I])
#        print 'Psi = %s' % Psi, Pi[I],
        cumulative_sum = 0
        for j in range(len(Pi[I])):
            J = j
            cumulative_sum += Pi[I][j]
            if cumulative_sum > Psi:
                break
#        print 'J = %s' % J
        
        mu = L[I][J]
#        print 'mu = %s' % mu, '(%s)' % reactions[mu], I, Sigma[I]
        
        '''
        Sample tau: generate a uniform random number r_2 between 0 and 1 and compute
        the time to the next reaction tau as tau <- a^-1 * ln(r_2^-1)
        '''
        r_2 = random()
#        print 'a = %s, r_2=%s' % (a, r_2)
        tau = a ** -1 * log(r_2 ** -1)
        if tau <= 0:
            raise ValueError
#        print 'tau:', tau
        
        '''
        4. Update n: for each index k of U1_mu, l <- U1_u,k and n_l <- n_l+U2_u,k
        '''
        print reactions[mu],
        print n, '->',
        for k, l in enumerate(U1[mu]):
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
#            print 'l = %s' % l, '# index of species in reaction %s' % mu  
            
            # 5.2. For each index m of U3_l, do:
            for i, j in U3[l]: # 5.2.1
                if i == 0:
                    raise ValueError
                
                # skips zeroth and first order reactions because they are not in U3
#                print '(i, j) = %s' % ((i, j),), '# major and minor indices of partial propensity in Pi'

                # 5.2.2 and 5.2.3
#                print
#                print 'U2[%d][%d] = %s' % (mu, k, U2[mu][k])
#                print 'Pi[%d][%d] = %s, Lambda[%d] = %s' % (i, j, Pi[i][j], i, Lambda[i]) 
                if l + 1 != i: #XXX l needed incrementing, not i!
                    delta_Pi_i_j = reactions[mu].constant * U2[mu][k]
                else:
                    delta_Pi_i_j = 0.5 * reactions[mu].constant * U2[mu][k] 
#                print 'delta_Pi_i_j = %s, l != i = %s' % (delta_Pi_i_j, l != i) 
                Pi[i][j] += delta_Pi_i_j
                Lambda[i] += delta_Pi_i_j
#                print 'Pi[%d][%d] = %s, Lambda[%d] = %s' % (i, j, Pi[i][j], i, Lambda[i]) 
                
                
                # 5.2.4
                Sigma_temp = Sigma[i]
#                print 'Sigma_temp = %s' % Sigma_temp
                
                # 5.2.5
                Sigma[i] = n[i - 1] * Lambda[i]
#                print 'Sigma[i] = %s' % Sigma[i]
                
                # 5.2.6
                delta_a += Sigma[i] - Sigma_temp
#                print 'delta_a = %s' % delta_a
                    
#                print_Sigma_n_Lambda_Pi()
            
            # 5.3
#            print 'l = %s' % l
#            print 'n[l] = %s' % n[l]
#            print 'Lambda[l] = %s' % Lambda[l]
#            print 'Sigma[l] = %s' % Sigma[l]
            # fails here with only source reactions because there is no
            # Lambda or Sigma group indexed by l 
            delta_a += n[l] * Lambda[l + 1] - Sigma[l + 1]
#            print 'delta_a = %s' % delta_a
            Sigma[l + 1] = n[l] * Lambda[l + 1]
#            print 'Sigma[l] = %s' % Sigma[l]
        
        assert Lambda[0] == Lambda_0
        assert Sigma[0] == Sigma_0
        
        '''
        6. Update a and increment time: 
            a <- a + delta_a; 
            delta_a <- 0; 
            t <- t + tau
        '''
        a += delta_a
#        print 'a = %s' % a

        delta_a = 0
        
        t += tau

        '''
        7. Go to step 2
        '''

        reactions_performed += 1
#        print '%d reactions performed' % reactions_performed

        compare_Pi()
        
        a0 = DM_a0()
        print a, a0
#        if t > 0:
#            print reactions[mu], n
        assert a == a0
            
        
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
        'S1':10,
        'S2':10,
        'S3':10,
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
    simulation = PDM(reactions, state, t_f=100)

debug = True
if __name__ == '__main__':
    main()
    

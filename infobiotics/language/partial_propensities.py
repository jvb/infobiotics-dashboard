'''Implementation of Partial-propensities Direct Method from Ramaswamy 2009.

asserts can be excluded by running script with 'python -O script_name.py' 
'''
from __future__ import division # because Python 2.x does floor-division by default!
from math import log # tau
from random import random # r_1 and r_2
from multiset import multiset # reactants and products in reaction class

# demonstrate difference between len and cardinality of multiset
m = multiset({'S1': 2}) # multiset created from dictionary
assert len(m) == 1 # one type of species
assert m.cardinality() == 2 # two items in multiset
del m

class reaction(object):
    def __init__(self, reactants, products, constant):
        self.reactants = multiset(reactants)
        self.products = multiset(products)
        self.constant = float(constant)
    def __str__(self):
        '''Called when reaction is interpreted as a string.'''
        return '%s -> %s' % (self.reactants, self.products)
    def __repr__(self):
        '''Called when, for instance, a sequence of reactions are interpreted 
        as a string.'''
        return str(self)

def PDM(reactions, state, t_f):
    '''Simulate system using Partial-propensities Direct Method, where 
    reactions is a list of reaction objects, state is a multiset of species 
    quantities and t_f is the maximum simulated time (in same time units as the 
    reactions stochastic rate constants).'''
    
    def print_reactions():
        for i, r in enumerate(reactions):
            print 'R_%s =' % (i), r
        print
    
    # add missing species (from reactions) to state
    for r in reactions:
        for s in r.reactants.keys() + r.products.keys(): # keys are species names
            try:
                _ = state[s]
            except KeyError:
                state[s] = 0
    species = sorted(state.keys())

    def print_species():
        for i, s in enumerate(species):
            print s, '=', n[i]
        print

    N = len(species)#; M = len(reactions) # M not used

    # 1 
    t = 0

    n = [state[s] for s in species] # state vector

    def initialize_Pi_L_U3_Lambda_Sigma(n=n):
        '''Factored out into function so we can test current Pi against a Pi 
        initialized from any state vector(n).'''
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
    
    if __debug__:
        Sigma_0 = Lambda_0 = Sigma[0]

    def compare_Pi(Pi1=Pi):
        Pi2, _, _, Lambda, Sigma = initialize_Pi_L_U3_Lambda_Sigma()
        try:
            for i, Pi1_i in enumerate(Pi1):
                for j, Pi1_i_j in enumerate(Pi1_i):
                    assert Pi1_i_j == Pi2[i][j]
        except AssertionError:
            print 'actual:'
            print_Sigma_n_Lambda_Pi(Sigma, Lambda, Pi1)
            print 'correct:'
            print_Sigma_n_Lambda_Pi(Sigma, Lambda, Pi2)
            print 'difference:'
            print 'i = %s, j = %s, actual = %s, correct = %s' % (i, j, Pi1_i_j, Pi2[i][j])
            
    if __debug__:
        compare_Pi()
    
    def print_Pi_Lambda_Sigma():
        for i, outer in enumerate(Pi):
            print 'Pi_%s =' % i,
            for inner in outer:
                print inner,
            print
        print
        for i, outer in enumerate(Lambda):
            print 'Lambda_%s =' % i, outer
        print
        for i, outer in enumerate(Sigma):
            print 'Sigma_%s =' % i, outer

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

    def DM_a0():
        '''Calculates total propensity using Gillespie's Direct Method'''
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
    
    def print_L_U1_U2_U3():
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

    reactions_performed = 0
    while a > 0 and t < t_f:
        print 'time %f' % t, n,

        # 2
        r_1 = random()
        r_1a = r_1 * a
        cumulative_sum = 0
        for i, sigma in enumerate(Sigma):
            I = i
            cumulative_sum += sigma
            if cumulative_sum > r_1a:
                break
        
        Phi = sum(Sigma[:I + 1])
        if I > 0: # avoid divide by zero (not mentioned in paper!)
            Psi = (r_1a - Phi + Sigma[I]) / n[I - 1]
        else:
            Psi = (r_1a - Phi + Sigma[I])
        cumulative_sum = 0
        for j in range(len(Pi[I])):
            J = j
            cumulative_sum += Pi[I][j]
            if cumulative_sum > Psi:
                break
        
        mu = L[I][J]
        
        '''
        Sample tau: generate a uniform random number r_2 between 0 and 1 and compute
        the time to the next reaction tau as tau <- a^-1 * ln(r_2^-1)
        '''
        r_2 = random()
        tau = a ** -1 * log(r_2 ** -1)
        assert tau > 0
        
        # 4
        for k, l in enumerate(U1[mu]):
            n[l] += U2[mu][k]
            assert n[l] >= 0 # negative species are not allowed
        
        # 5
        for k, l in enumerate(U1[mu]): 
            
            # 5.1 
            #l = U1[mu][k] # done above 
            
            # 5.2
            for i, j in U3[l]: # 5.2.1
                assert i != 0
                
                # 5.2.2 and 5.2.3
                if l + 1 != i: # l needed incrementing, not i, because
                    delta_Pi_i_j = reactions[mu].constant * U2[mu][k]
                else:
                    delta_Pi_i_j = 0.5 * reactions[mu].constant * U2[mu][k] 
                Pi[i][j] += delta_Pi_i_j
                Lambda[i] += delta_Pi_i_j
                
                # 5.2.4
                Sigma_temp = Sigma[i]
                
                # 5.2.5
                Sigma[i] = n[i - 1] * Lambda[i]
                
                # 5.2.6
                delta_a += Sigma[i] - Sigma_temp
            
            # 5.3
            delta_a += n[l] * Lambda[l + 1] - Sigma[l + 1]
            Sigma[l + 1] = n[l] * Lambda[l + 1]
        
        assert Lambda[0] == Lambda_0 # Lambda[0] should never change
        assert Sigma[0] == Sigma_0 # Sigma[0] should never change
        assert Lambda[0] == Sigma[0] # Lamda[0] and Sigma[0] should be equal 
        
        # 6
        a += delta_a
        delta_a = 0
        t += tau
        
        if __debug__:
            a0 = DM_a0()
            try:
                assert a == DM_a0()
            except AssertionError, e:
                print 'Total propensity (a) = %s' % a
                print 'DM propensity (a0) = %s' % a0
                compare_Pi()
                raise AssertionError, e

        reactions_performed += 1
        if t > 0:
            print 'reaction %s: %s' % (reactions_performed, reactions[mu])

        # 7
        # loop
            
    print 'time %f' % t, n
    print 'done'
    

def main():
  
    reactions = [
        reaction(['S1', 'S2'], ['S3'], 1),
        reaction([], ['S1'], 1),
        reaction(['S2', 'S2'], ['S1'], 1),
        reaction(['S3'], [], 1),
        reaction(['S1', 'S3'], ['S2'], 1),
    ]
    
    state = multiset({
        'S1':10,
        'S2':10,
        'S3':10,
    })
    
#    reactions = [
#        reaction([], ['a'], 1),
#        reaction(['a'], ['a'], 1),
#        reaction([], ['b'], 1),
#        reaction([], ['c'], 1),
#    ]
    
#    simulation = PDM()
#    simulation.initialize(reactions, state)
#    simulation.run()
    PDM(reactions, state, t_f=100)


if __name__ == '__main__':
    main()

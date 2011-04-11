'''Implementation of Partial-propensities Direct Method from Ramaswamy 2009.

asserts can be excluded by running script with 'python -O script_name.py' 
'''
from __future__ import division # because Python 2.x does floor-division by default!
from math import log # tau
from random import random # r_1 and r_2
from multiset import multiset#, frozenmultiset # reactants and products in reaction class
from infobiotics.commons.orderedset import OrderedSet
## demonstrate difference between len and cardinality of multiset
#m = multiset({'S1': 2}) # multiset created from dictionary
#assert len(m) == 1 # one type of species
#assert m.cardinality() == 2 # two items in multiset
#del m

class reaction(object):
    def __init__(self, reactants, products, constant):
        self.reactants = multiset(reactants)
        self.products = multiset(products)
        self.constant = float(constant)
    def __str__(self):
        '''Called when reaction is interpreted as a string.'''
        return '%s %s-> %s' % (self.reactants, self.constant, self.products)
    def __repr__(self):
        '''Called when, for instance, a sequence of reactions are interpreted 
        as a string, e.g. print [r1, r2]'''
        return str(self)
    def __eq__(self, other):
        return True if hash(self) == hash(other) else False
    def __hash__(self):
        return hash(str(self))

def PDM(reactions, state, t_f):
    '''Simulate system using Partial-propensities Direct Method, where 
    reactions is a list of reaction objects, state is a multiset of species 
    quantities and t_f is the maximum simulated time (in same time units as the 
    reactions stochastic rate constants).'''
    
    def print_reactions():
        for i, r in enumerate(reactions):
            print 'R_%s =' % (i), r
        print

    reactions = list(OrderedSet(reactions))

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
            c = r.constant
            cardinality = r.reactants.cardinality()
            if cardinality == 0:
                Pi[0].append(c)
                L[0].append(i)
                continue
            else:
                reactants = r.reactants.keys()
            if cardinality == 1:
                reactant_index = species.index(reactants[0])
                pi = c
            elif cardinality == 2:
                if len(reactants) == 2:
                    # heterogenous
                    reactant_indices = [species.index(s) for s in reactants] 
                    reactant_index = min(reactant_indices)
                    dependant_index = max(reactant_indices)
                    pi = c * n[dependant_index]
                else:
                    # homogenous
                    reactant_index = species.index(reactants[0])
                    dependant_index = reactant_index
                    pi = c * 0.5 * (n[reactant_index] - 1)
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
        Pi2 = initialize_Pi_L_U3_Lambda_Sigma()[0]
        differences = []
        try:
            for i, Pi1_i in enumerate(Pi1):
                for j, Pi1_i_j in enumerate(Pi1_i):
                    if not Pi1_i_j == Pi2[i][j]:
                        differences.append((i, j))
            if len(differences) > 0:
                raise AssertionError
        except AssertionError:
            print 'actual:'
            print_Sigma_n_Lambda_Pi()
            print 'correct:'
            _, _, _, Lambda, Sigma = initialize_Pi_L_U3_Lambda_Sigma()
            print_Sigma_n_Lambda_Pi(Sigma, Lambda, Pi2)
            for i, j in differences:
                print 'difference:'
                print 'i = %s, j = %s, actual = %s, correct = %s' % (i, j, Pi1[i][j], Pi2[i][j])
            raise AssertionError, e
            
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
        p = 0
        for r in reactions:
            a0 += p
            c = r.constant
            cardinality = r.reactants.cardinality()
            if cardinality == 0:
                p = c
                continue
            reactants = r.reactants.keys()
            if cardinality == 1:
                p = c * n[species.index(reactants[0])]
            elif cardinality == 2:
                n_i = n[species.index(reactants[0])]
                if len(reactants) == 1:
                    # homo
                    p = c * 0.5 * n_i * (n_i - 1)
                else:
                    # hetero
                    p = c * n_i * n[species.index(reactants[1])]
#            print n, reactants, c, p
        a0 += p
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

    # debugging Daven's example
    print_L_U1_U2_U3()
    print
    print_Sigma_n_Lambda_Pi()

    print
    print 'reactions time     state'
    reactions_performed = 0
    while a > 0:
        iteration = '%s%f %s' % (str(reactions_performed).ljust(10), t, n)
        if t > 0:
            print '%s\t%s' % (iteration, reactions[mu]) #@UndefinedVariable
        else:
            print iteration
        reactions_performed += 1

        # 2
        # I
        r_1 = random()
        r_1a = r_1 * a
        cumulative_sum = 0
        for i, sigma in enumerate(Sigma):
            I = i
            cumulative_sum += sigma
            if cumulative_sum > r_1a:
                break
        # J
        Phi = sum(Sigma[:I + 1])
        if I > 0: # avoid divide by zero for source reactions (not in paper!)
            Psi = (r_1a - Phi + Sigma[I]) / n[I - 1]
        else:
            Psi = (r_1a - Phi + Sigma[I])
        cumulative_sum = 0
        for j in range(len(Pi[I])):
            J = j
            cumulative_sum += Pi[I][j]
            if cumulative_sum > Psi:
                break
        # mu (the index of the next reaction to apply)
        mu = L[I][J]
        
#        mu = 2
        
        # 3
        r_2 = random()
        tau = a ** -1 * log(r_2 ** -1)
        assert tau > 0
        t += tau
        if t > t_f:
            # finish before applying reaction because time is up
            break
        
        # 4
        for k, l in enumerate(U1[mu]):
            n[l] += U2[mu][k]
            assert n[l] >= 0 # negative species are not allowed
        
        # 5
        for k, l in enumerate(U1[mu]): 
            
            # 5.1 
            #l = U1[mu][k] # done above 
#            print 'k =', k 
#            print 'l =', l, '(l + 1 = %s)' % (l + 1) 
#            print 'mu =', mu 
#            print 'reactions[mu].constant =', reactions[mu].constant
            
            # 5.2
            for i, j in U3[l]: # 5.2.1
                assert i != 0
                
#                c = reactions[mu].constant
                c = reactions[L[i][j]].constant # not mentioned in paper, fixes algorithm
                
                # 5.2.2 and 5.2.3
                if l + 1 != i: # l needed incrementing, not i, because
                    delta_Pi_i_j = c * U2[mu][k]
                else:
                    delta_Pi_i_j = 0.5 * c * U2[mu][k] 
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
        assert Lambda[0] == Sigma[0] # Lambda[0] and Sigma[0] should be equal 
        
        # 6
        a += delta_a
        delta_a = 0
        #t += tau # done in 3
        
        if __debug__:
            # compare total propensities to Direct Method
            a0 = DM_a0()
            try:
                assert a == DM_a0()
            except AssertionError, e:
                print '^'
                print 'Total propensity (a) = %s' % a
                print 'DM propensity (a0) = %s' % a0
                compare_Pi()
                
        # 7
        # loop


def PDM2(reactions, state, t_f):
    '''Simulate system using Partial-propensities Direct Method, where 
    reactions is a list of reaction objects, state is a multiset of species 
    quantities and t_f is the maximum simulated time (in same time units as the 
    reactions stochastic rate constants).'''
    
    # remove duplicate reactions
    reactions = list(OrderedSet(reactions))

    # add missing species (from reactions) to state
    for r in reactions:
        for s in r.reactants.keys() + r.products.keys(): # keys are species names
            try:
                _ = state[s]
            except KeyError:
                state[s] = 0

    # extract species from state
    species = sorted(state.keys())

    # remember total number of species
    N = len(species)

    # create initial state vector from state and species
    n = [state[s] for s in species]

    U3 = [[] for _ in range(N)] # species to partial propensities dependency graph 
    Pi = [[] for _ in range(N + 1)] # partial properties
    L = [[] for _ in range(N + 1)] # look-up table of partial-propensities to reaction indices
    C = [[] for _ in range(N + 1)] # partial propensities reactions constants
    for i, r in enumerate(reactions):
        c = r.constant
        cardinality = r.reactants.cardinality()
        if cardinality == 0:
            Pi[0].append(c)
            L[0].append(i)
            C[0].append(c)
            continue
        else:
            reactants = r.reactants.keys()
        if cardinality == 1:
            reactant_index = species.index(reactants[0])
            pi = c
        elif cardinality == 2:
            if len(reactants) == 2: 
                # heterogenous
                reactant_indices = [species.index(s) for s in reactants] 
                reactant_index = min(reactant_indices)
                dependant_index = max(reactant_indices)
                pi = c * n[dependant_index]
            else:
                # homogenous
                reactant_index = species.index(reactants[0])
                dependant_index = reactant_index
                pi = c * 0.5 * (n[reactant_index] - 1)
        Pi_index = reactant_index + 1 
        Pi[Pi_index].append(pi)
        L[Pi_index].append(i)
        C[Pi_index].append(c)
        if cardinality == 2: 
            U3[dependant_index].append((Pi_index, len(Pi[Pi_index]) - 1))
        
    Lambda = [sum(pies) if len(pies) > 0 else 0 for pies in Pi]

    Sigma = [Lambda[0]]
    for i, n_i in enumerate(n):
        Sigma.append(n_i * Lambda[i + 1])
    
    # U1 and U2 are sparse representations of the stoichometric matrix
    # array of M arrays, where the ith array contains the indices of all species involved in the ith reaction'
    U1 = [[species.index(s) for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]
    # array of M arrays contains the corresponding stoichiometry (change in population of each species upon reaction) of the species references by U1
    U2 = [[r.products[s] - r.reactants[s] for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]
    
    print 'reactions time     state'
    reactions_performed = 0
    t = 0
    a = sum(Sigma)
    while a > 0:
        delta_a = 0
        iteration = '%s%f %s' % (str(reactions_performed).ljust(10), t, n)
        if t > 0:
            print '%s\t%s' % (iteration, reactions[mu]) #@UndefinedVariable
        else:
            print iteration
        reactions_performed += 1
        # I
        r_1 = random()
        r_1a = r_1 * a
        cumulative_sum = 0
        for i, sigma in enumerate(Sigma):
            I = i
            cumulative_sum += sigma
            if cumulative_sum > r_1a:
                break
        # J
        Phi = sum(Sigma[:I + 1])
        if I > 0: # avoid divide by zero for source reactions (not in paper!)
            Psi = (r_1a - Phi + Sigma[I]) / n[I - 1]
        else:
            Psi = (r_1a - Phi + Sigma[I])
        cumulative_sum = 0
        for j in range(len(Pi[I])):
            J = j
            cumulative_sum += Pi[I][j]
            if cumulative_sum > Psi:
                break
        mu = L[I][J] # the index of the next reaction to apply
        r_2 = random()
        tau = a ** -1 * log(r_2 ** -1)
        t += tau
        if t > t_f:
            break
        for k, l in enumerate(U1[mu]):
            n[l] += U2[mu][k]
        for k, l in enumerate(U1[mu]): 
            l_ = l + 1
            for i, j in U3[l]: # 5.2.1
                c = C[i][j]
                if l_ != i:
                    delta_Pi_i_j = c * U2[mu][k]
                else:
                    delta_Pi_i_j = 0.5 * c * U2[mu][k] 
                Pi[i][j] += delta_Pi_i_j
                Lambda[i] += delta_Pi_i_j
                Sigma_temp = Sigma[i]
                Sigma[i] = n[i - 1] * Lambda[i]
                delta_a += Sigma[i] - Sigma_temp
            delta_a += n[l] * Lambda[l_] - Sigma[l_]
            Sigma[l_] = n[l] * Lambda[l_]
        a += delta_a


# run on example in paper
reactions = [
    reaction(['S1', 'S2'], ['S3'], 1),
#    reaction([], ['S1'], 2),
    reaction(['S2', 'S2'], ['S1'], 3),
    reaction(['S3'], [], 4),
    reaction(['S1', 'S3'], ['S2'], 5),
]

state = multiset({
    'S1':100,
    'S2':200,
    'S3':300,
})

PDM2(reactions, state, t_f=1)

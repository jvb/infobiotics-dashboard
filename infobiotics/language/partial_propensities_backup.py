'''Implementation of Partial-propensities Direct Method from Ramaswamy 2009.

asserts can be excluded by running script with 'python -O script_name.py' 
'''
from __future__ import division # because Python 2.x does floor-division by default!
from math import log # tau
import random # r_1 and r_2
from infobiotics.commons.multiset import multiset # reactants and products in reaction class
from infobiotics.commons.orderedset import OrderedSet

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


def PDM(reactions, state, t_f, seed=None):
    '''Simulate system using Partial-propensities Direct Method, where 
    reactions is a list of reaction objects, state is a multiset of species 
    quantities and t_f is the maximum simulated time (in same time units as the 
    reactions stochastic rate constants).'''
    random.seed(seed)
    
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
    
    # create initial state vector from state and species
    n = [state[s] for s in species]

    N = len(species) # total number of species
    N_ = N + 1 # total number of species + 1 row for source reactions
    U3 = [[] for _ in range(N)] # species to partial propensities dependency graph 
    Pi = [[] for _ in range(N_)] # partial properties
    L = [[] for _ in range(N_)] # look-up table of partial-propensities to reaction indices
    C = [[] for _ in range(N_)] # partial propensities reactions constants
    for i, r in enumerate(reactions):
        c = r.constant
        number_of_reactants = r.reactants.cardinality()
        if number_of_reactants == 0:
            Pi[0].append(c)
            L[0].append(i)
            C[0].append(c)
            continue
        else:
            reactants = r.reactants.keys()
        if number_of_reactants == 1:
            reactant_index = species.index(reactants[0])
            pi = c
        elif number_of_reactants == 2:
            if len(reactants) == 2:
                # heterogenous
                reactant_indices = [species.index(s) for s in reactants] 
                reactant_index = min(reactant_indices)
                dependant_index = max(reactant_indices)
                pi = c * n[dependant_index]
            else:
                # homogenous
                dependant_index = reactant_index = species.index(reactants[0])
                pi = c * 0.5 * (n[reactant_index] - 1)
        Pi_index = reactant_index + 1 
        Pi[Pi_index].append(pi)
        L[Pi_index].append(i)
        C[Pi_index].append(c)
        if number_of_reactants == 2: 
            U3[dependant_index].append((Pi_index, len(Pi[Pi_index]) - 1))
        
    # initialize Lambda - the sum of the partial propensities
    Lambda = [sum(pi_i) if len(pi_i) > 0 else 0 for pi_i in Pi]

    # initialize Sigma - the sums of the propensities
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
        r_1 = random.random()
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
        
        # the time to apply it
        r_2 = random.random()
        tau = a ** -1 * log(r_2 ** -1)
        t += tau
        if t > t_f:
            break
        
        # update state
        for k, l in enumerate(U1[mu]):
            n[l] += U2[mu][k]
        
        # update partial-propensities
        for k, l in enumerate(U1[mu]): 
            l_ = l + 1
            for i, j in U3[l]:
                c = C[i][j] # constant of the partial-propensity
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
    reaction([], ['S1'], 2),
    reaction(['S2', 'S2'], ['S1'], 3),
    reaction(['S3'], [], 4),
    reaction(['S1', 'S3'], ['S2'], 5),
]

state = multiset({
    'S1':10,
    'S2':20,
    'S3':30,
})

PDM(reactions, state, t_f=1, seed=1)

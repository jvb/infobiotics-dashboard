from math import log

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
        return '"%s: %s -> %s"' % (self.id, self.reactants, self.products)
    def __repr__(self):
        return str(self)
    

class PDM(object):
    
#    def initialize(self, reactions, state):
    def __init__(self, reactions, state, t_f):
        '''Initialize compartment where reactions is a list of reaction objects
        and state is a dictionary of species amounts.'''
        
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
#        print '\nn:'
#        print n

        U3 = [[] for _ in n]

        # initialize Pi and L
        for i, r in enumerate(reactions):
            r.index = i
        rs = reactions[:] # make a copy reactions which we can empty
        # copy constants of source (zeroth-order) reactions into Pi
        # do this is in reverse so we can remove them without skipping items 
        sources = []
        sources_L = []
        for r in reversed(rs):
            cardinality = r.reactants.cardinality()
            if cardinality == 0:
                sources.append(r.constant)
                sources_L.append(r.index)
                rs.remove(r)
        Pi = [sources]
        L = [sources_L]
        Pi_map = {} # used to know where to put pi (partial propensities)
        Lambda_to_n = []
        for r in rs:
            cardinality = r.reactants.cardinality()
            reactants = r.reactants.keys()
            if cardinality == 1:
                reactant = reactants[0]
                pi = r.constant
                i = species.index(reactant)
            elif cardinality == 2:
                if len(reactants) == 2:
                    # heterogenous
                    i = min(species.index(s) for s in reactants)
                    reactant = species[i]
                    dependant = species[max(species.index(s) for s in reactants)]
                    pi = r.constant * n[max(species.index(s) for s in reactants)]
                else:
                    # homogenous
                    reactant = reactants[0]
                    dependant = reactants[0]
                    i = species.index(reactant)
                    pi = r.constant * 0.5 * (n[species.index(reactant)] - 1)
            try:
                index = Pi_map[reactant]
                Pi[index].append(pi)
                L[index].append(r.index)
            except KeyError:
                Pi_map[reactant] = len(Pi)
                index = Pi_map[reactant] 
                Pi.append([pi])
                L.append([r.index])
                Lambda_to_n.append(i)
            if cardinality == 2: 
                U3[species.index(dependant)].append((index, len(Pi[index]) - 1))
#        print '\nPi:'
#        for outer in Pi:
#            for inner in outer:
#                print inner,
#            print
        print '\nL:'
        for outer in L:
            for inner in outer:
                print inner,
            print
            
        # initialize Lambda
        Lambda = [sum(pies) for pies in Pi]
#        print '\nLambda:'
#        for outer in Lambda:
#            print outer

        # initialize Sigma
        Sigma = [n[Lambda_to_n[i - 1]] * lamb if i > 0 else Lambda[0] for i, lamb in enumerate(Lambda)]
#        print '\nSigma:'
#        for outer in Sigma:
#            print outer

        a = sum(Sigma)
        
        delta_a = 0
        
        U1 = [[species.index(s) for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]
#        print '\nU1:'
#        for outer in U1:
#            for inner in outer:
#                print inner,
#            print

        U2 = [[r.products[s] - r.reactants[s] for s in sorted(r.reactants.keys() + r.products.keys())] for r in reactions]
#        print '\nU2:'
#        for outer in U2:
#            for inner in outer:
#                print inner,
#            print
        
#        U3 = [[] for _ in n]
#        Pi_map_inverted = dict((value, key) for key, value in Pi_map.iteritems())
#        for k, s in enumerate(species):
#            for i, outer in enumerate(Pi):
#                for j, inner in enumerate(outer):
#                    if len(inner.args) > 1:
#                        if Pi_map_inverted[inner.args[1]] == s:
#                            U3[k].append((i, j))
#        print '\nU3:'
#        for outer in U3:
#            for inner in outer:
#                print inner,
#            print

#    def run(self, t_f):

        from random import random
        reactions_performed = 0
        while t < t_f:
#        while reactions_performed < 10:
            reactions_performed += 1
            print '%f' % t, n,
    
            '''
            2. Sample mu: generate a uniform random number r_1 between 0 and 1 and 
            determine the group index I and the element index J according to Eqs. (2), (4),
            and (5); mu <- L_IJ
            '''
            r_1 = random()
            r_1a = r_1 * a
            cumulative_sum = 0
            for i, sigma in enumerate(Sigma):
                cumulative_sum += sigma
                if cumulative_sum > r_1a:
                    break
            I = i
#            print 'I:', I
            
            #J
            Phi = sum(Sigma[0:I + 1])
            Psi = (r_1a - Phi + Sigma[I]) / n[I] #FIXME going to divide by zero
            cumulative_sum = 0
            for j in range(len(Pi[I])):
                cumulative_sum += Pi[I][j]
                if cumulative_sum > Psi:
                    break
            J = j
#            print 'J:', J
            
            mu = L[I][J]
            print 'mu:', mu
            
            '''
            Sample tau: generate a uniform random number r_2 between 0 and 1 and compute
            the time to the next reaction tau as tau <- a^-1 * ln(r_2^-1)
            '''
            r_2 = random()
            tau = a ** -1 * log(r_2 ** -1)
#            print 'tau:', tau
            
            '''
            4. Update n: for each index k of U1_mu, l <- U1_u,k and n_l <- n_l+U2_u,k
            '''
            for k, _ in enumerate(U1[mu]):
                l = U1[mu][k]
                n[l] += U2[mu][k]

            '''
            5. Update Pi, Lambda, Sigma and compute delta_a, the change in a:
                For each index k of U1_mu, do:
            '''
            for k, _ in enumerate(U1[mu]): # 5.1
                l = U1[mu][k]
                for m, _ in enumerate(U3[l]): # 5.2. For each index m of U3_l, do: # skips zeroth and first order rxns
                    # 5.2.1
                    i, j = U3[l][m] 
                    # 5.2.2
                    if l != i: 
                        # hetero
                        Pi[i][j] += reactions[mu].constant * U2[mu][k] 
                    else:
                        # homo
                        Pi[i][j] += 0.5 * reactions[mu].constant * U2[mu][k] 
                    # 5.2.3
                    if l != i: 
                        # hetero
                        Lambda[i] += reactions[mu].constant * U2[mu][k] 
                    else:
                        # homo
                        Lambda[i] += 0.5 * reactions[mu].constant * U2[mu][k] 
                    # 5.2.4
                    Sigma_temp = Sigma[i]
                    # 5.2.5
                    Sigma[i] = n[i] * Lambda[i]
                    # 5.2.6
                    delta_a += Sigma[i] - Sigma_temp
                # 5.3
                delta_a += n[l] * Lambda[l] - Sigma[l]
                Sigma[l] = n[l] * Lambda[l]
            
            '''
            6. Update a and increment time: a <- a + delta_a; delta_a <- 0; t <- t + tau
            '''
            a += delta_a
            delta_a = 0
            t += tau
            
            '''
            7. Go to step 2
            '''
            
#            t += t_f # safety measure


def main():
  
    c1 = 1
    c2 = 1
    c3 = 1
    c4 = 1
    c5 = 1
#    R1 = reaction(['S1', 'S2'], ['S3'], c1)
#    R2 = reaction([], ['S1'], c2)
#    R3 = reaction(['S2', 'S2'], ['S1'], c3)
#    R4 = reaction(['S3'], [], c4)
#    R5 = reaction(['S1', 'S3'], ['S2'], c5)
#    reactions = [R1, R2, R3, R4, R5]
    reactions = [
        reaction(['S1', 'S2'], ['S3'], c1),
        reaction([], ['S1'], c2),
        reaction(['S2', 'S2'], ['S1'], c3),
        reaction(['S3'], [], c4),
        reaction(['S1', 'S3'], ['S2'], c5),
    ]
    
    state = {
        'S1':10,
        'S2':20,
        'S3':30,
    }
    
#    simulation = PDM()
#    simulation.initialize(reactions, state)
#    simulation.run()
    simulation = PDM(reactions, state, t_f=10)


if __name__ == '__main__':
    main()
    

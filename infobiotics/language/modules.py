from api import Rule

def Deg(reactant, label, constant):
    ''' Degradation of a single molecule within a compartment. '''
    return Rule(
        reactantsInside={reactant:1},
        reactantsLabel=label,
        productsLabel=label,
        constant=constant,
    )
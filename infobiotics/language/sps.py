from enthought.traits.api import HasTraits, Str, List, Instance, Property, Dict, Int, Either, Float, Tuple
from rule import Rule
from infobiotics.commons.sequences import flatten

class Compartment(HasTraits):
    label = Str
    
class SPsystem(HasTraits):
    name = Str
    def _name_default(self):
        return self.__class__.__name__
    
    compartments = List(Compartment)

    initialMultisets = Dict(Str, Dict(Str, Int))
    
    ruleSets = Dict(Str, List(Either([Rule, List, Tuple]))) #TODO flatten before use

    flattened_ruleSets = Property(Dict(Str, List(Rule)), depends_on='ruleSets')
    def _get_flattened_ruleSets(self):
        return dict([(label, flatten(list)) for label, list in self.ruleSets.iteritems()])

    alphabet = Property(depends_on='flattened_ruleSets')
    def _get_alphabet(self):
        alphabet = set()
        for _, list in self.flattened_ruleSets.iteritems():
            for rule in list:
                for k in rule.reactantsOutside.keys() + rule.reactantsInside.keys() + rule.productsOutside.keys() + rule.productsInside.keys():
                    alphabet.add(k)
        return alphabet


#class Module(HasTraits):
#    objects = List(Str)
#    constants = List(Float)
#    labels = List(Str)
    
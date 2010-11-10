from sbml import Rule
from enthought.traits.api import HasTraits, List, Str, This
from infobiotics.commons.sequences import flatten

class Module(HasTraits):
    rules = List('Rule')
    modules = List(This)
    def get_rules(self):
        rules = self.rules
        for module in self.modules:
            rules.append(module.get_rules())
        return rules

class Module1(Module):
    rules = [
        Rule(reactants_inside='a', products_inside='b'),
    ]

def module(a):
    return Module(
        rules=[
            Rule(reactants_inside=a, products_inside='d'),
            Rule(reactants_inside='e', products_inside='f'),
        ],
        modules=[
            Module1(),
        ]
    )

#class Compartment(Module2, Module1):
#    pass
#
#c = Compartment()
#
# can't use multiple inheritance because declared traits because only first superclasses rules trait value inherited


class Compartment(HasTraits):
    rules = List('Rule')
    modules = List(Module)
    def __init__(self, **traits): # must add rules from modules in __init__ to make use of declaratively 
        super(Compartment, self).__init__(**traits)
        for module in self.modules:
            self.rules.append(module.get_rules())
        self.rules = flatten(self.rules)

class C(Compartment):
    modules = [
#        Module1(a='b'),
#        Module2(),
        module('b'),
    ]

c = C()
print len(c.rules)
for rule in c.rules:
    print rule.reactants_inside, rule.products_inside

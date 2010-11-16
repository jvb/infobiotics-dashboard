from infobiotics.commons.counter import Counter
class multiset(Counter):
    def __str__(self):
        ''' Returns 'a + b + b' for {'a':1,'b':2}. '''
        return ' + '.join([k for k, v in self.items() for _ in range(v)])

from quantities.quantity import Quantity
from id_generators import *
import re
from types import GeneratorType

class base(object):

    def __init__(self, name=None, id=None):
        if not hasattr(self, 'id_generator') and not isinstance(self.id_generator, GeneratorType):
            raise AttributeError('Subclasses of base must have an attribute "id_generator" that is a generator')
        self.id = id if id is not None else self.id_generator.next()
        self.name = name if name is not None else self.id


class species(base):

    id_generator = species_id_generator

    def __init__(self, amount=0, name=None, id=None):

        if isinstance(amount, int):
            self.amount = amount
        elif isinstance(amount, Quantity):
            print 'got here'
        else:
            raise ValueError('amount must be an integer (number of molecules) or a quantity (in units molecules, moles or molar concentration).')

        base.__init__(self, name, id)


class reaction(base):

    id_generator = reaction_id_generator

    matcher = re.compile('\s*((?P<id>\w+)\:)?\s*(?P<reactants_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<reactants_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<reactants_label>\w+)\s*-?(?P<rate_id>\w+)(->){1}\s*(?P<products_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<products_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<products_label>\w+)\s*(\w+)\s*\=\s*[-+]?(?P<rate>\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*')

    def __init__(self, reaction_or_name=None, id=None, **kwargs):

        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = 'l'
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = 'l'

        if reaction_or_name is not None:
            if isinstance(reaction_or_name, str):
                # attempt regex
                match = self.matcher.match(reaction_or_name)
                if match is not None:
                    match_groups_dict = match.groupdict()
                    for k, v in match_groups_dict.items():
                        if k == 'id' and v is not None:
#                            setattr(self, k, v)
                            id = v
                        elif k in ('reactants_outside', 'reactants_inside', 'products_outside', 'products_inside'):
                            if v is not None:
                                setattr(self, k, multiset([s.strip() for s in v.split('+')])) # can construct multiset from a list of str where the same str value might appear more than once
                            else:
                                setattr(self, k, multiset())
                        else:
                            setattr(self, k, v)
                    reaction_or_name = None
                else:
                    print 'Failed to create reaction from "%s"' % reaction_or_name

        for k, v in kwargs:
            setattr(self, k, v)

        base.__init__(self, reaction_or_name, id)

        if len(self.reactants_outside) > 2:
            raise ValueError('Too many reactants outside')
        elif len(self.reactants_inside) > 2:
            raise ValueError('Too many reactants inside')
        elif len(self.reactants_outside) + len(self.reactants_inside) > 2:
            raise ValueError('Too many reactants')

    def __str__(self):
        return '%s: %s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s = %s' % (
            self.id,
            self.reactants_outside,
            ' ' if len(self.reactants_outside) > 0 else '',
            self.reactants_inside,
            self.reactants_label,
            self.rate_id,
            self.products_outside,
            ' ' if len(self.products_outside) > 0 else '',
            self.products_inside,
            self.products_label,
            self.rate_id,
            self.rate,
        )


reserved_attribute_name_prefixes = ('_', 'name', 'id', 'id_generator')


class metacompartment(type):
    def __new__(self, name, bases, dictionary):
        ''' class c(compartment): a = 1, r1='...'
        
        Can directly alter dictionary. 
        
        Should be used for construction.
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        '''
        dictionary['id'] = name
        self.species = []
        self.reactions = []
        self.compartments = []
        for key, value in dictionary.items():
            if key.startswith(reserved_attribute_name_prefixes):
                continue
            if isinstance(value, (int, Quantity)): # convert int/Quantity to species
                s = species(value, id=key)
                dictionary[key] = s
                self.species.append(s)
            elif isinstance(value, (str)): # convert str to reaction
                r = reaction(value, id=key)
                if key != r.id:
                    if not r.id in dictionary:
                        dictionary[r.id] = r
#                    else:
#                        print 'Decided not to add reaction twice under name from string.'
                dictionary[key] = r
                self.reactions.append(r)
            elif isinstance(value, species):
                self.species.append(value)
            elif isinstance(value, reaction):
                self.reactions.append(value)
            elif isinstance(value, compartment):
                self.compartments.append(value)
        return super(metacompartment, self).__new__(self, name, bases, dictionary)


class compartment(base):
    __metaclass__ = metacompartment
#    import module_introspection.ply

    id_generator = compartment_id_generator

    volume = 1

    def __init__(self, name=None, id=None, **kwargs): #TODO *args for subcompartments?
        self.species = self.__class__.species[:]
        self.reactions = self.__class__.reactions[:]
        self.compartments = self.__class__.compartments[:]
        for k, v in kwargs.items():
            setattr(self, k, v)
        base.__init__(self, name, id)# if id is not None else self.__class__.__name__)

    def __setattr__(self, name, value):
        ''' compartment().a = 1 and compartment(a=1) '''
        if name.startswith(reserved_attribute_name_prefixes):
            super(compartment, self).__setattr__(name, value)
            return
        if isinstance(value, (int, Quantity)):
            value = species(value, id=name)
            self.species.append(value)
        elif isinstance(value, (str)):
            value = reaction(value, id=name)
            self.reactions.append(value)
        elif isinstance(value, species):
            self.species.append(value)
        elif isinstance(value, reaction):
            self.reactions.append(value)
        elif isinstance(value, compartment):
            self.compartments.append(value)
        super(compartment, self).__setattr__(name, value)

class subcompartment(compartment):
    # coerced to species or reaction by metacompartment.__new__
    a = 1
    r1 = 'r2: signal [receptor ]_bacteria -K_D-> [signal_receptor]_media K_D = 0.001'
    r2 = '[ ]_bacteria -k_production-> [signal_receptor]_media k_production = 0.001'


#print compartment.a.amount
#print compartment().a.amount
#print compartment(a=2).a.amount

#print compartment.species
#print compartment().species
#print compartment(b=2).species
##print compartment.r1

c = subcompartment(name='name')
print 'c.id', c.id
print 'c.name', c.name
c = subcompartment
print c.id
print c.reactions
print c.r1
print c.species
print c.compartments

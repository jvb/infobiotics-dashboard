from infobiotics.commons.quantities.api import *

from infobiotics.commons.counter import Counter
class multiset(Counter):
    def __str__(self):
        ''' Returns 'a + b + b' for {'a':1,'b':2}. '''
        return ' + '.join([k for k, v in self.items() for _ in range(v)])

from id_generators import *
import re
from types import GeneratorType
import itertools

class base(object):

    def __init__(self, name=None, id=None, **kwargs):
        if not hasattr(self, 'id_generator') and not isinstance(self.id_generator, GeneratorType):
            raise AttributeError('Subclasses of base must have an attribute "id_generator" that is a generator')
        self.id = id if id is not None else self.id_generator.next()
        self.name = name if name is not None else self.id
        for k, v in kwargs.items():
            setattr(self, k, v)

class species(base):

    id_generator = species_id_generator

    def __init__(self, amount=0 * molecules, name=None, id=None, **kwargs):

        if isinstance(amount, int):
            self.amount = amount * molecules
            self.is_concentration = False
        elif isinstance(amount, Quantity):
            # quantity.rescale() raises ValueError if conversion not possible
            try:
                amount.rescale('mole')
                self.amount = amount
                self.is_concentration = False
            except ValueError:
                try:
                    amount.rescale('molar')
                    self.amount = amount
                    self.is_concentration = True
                except ValueError:
                    raise ValueError('Dimensionality of species amount (%s) not in molar, moles or molecules.' % amount.dimensionality)
        else:
            raise ValueError('Species amount must be an integer (number of molecules) or a quantity (in units of molecules, moles or molar concentration).')

        base.__init__(self, name=name, id=id, **kwargs)

    def __str__(self):
        return '%s=%s' % (self.id, self.amount)

class reaction(base):

    id_generator = reaction_id_generator

    matcher = re.compile('\s*((?P<id>\w+)\:)?\s*(?P<reactants_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<reactants_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<reactants_label>\w+)\s*-?(?P<rate_id>\w+)(->){1}\s*(?P<products_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<products_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<products_label>\w+)\s*(\w+)\s*\=\s*[-+]?(?P<rate>\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*')

    def __init__(self, reaction_or_name=None, id=None, **kwargs):

        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = 'l' #TODO compartment
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = 'l'
        self.rate_id = 'k'
        self.rate = 0

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

        #TODO rate - see infobiotics.commons.quantities.units.calculators:conversion_function_from_units

        base.__init__(self, reaction_or_name, id, **kwargs)

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


reserved_attribute_name_prefixes = ('_', 'name', 'id', 'id_generator', 'volume')

class compartment(base): pass

class metacompartment(type):
    def __new__(self, name, bases, dictionary):
        ''' class c(compartment): a = 1, r1='...'
        
        Can directly alter dictionary. 
        
        Should be used for construction.
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        '''
        dictionary['id'] = name
        self._species = []
        self._reactions = []
        self._compartments = []
        for key, value in dictionary.items():
            if key.startswith(reserved_attribute_name_prefixes):
                continue
            if isinstance(value, (int, Quantity)): # convert int/Quantity to species
                s = species(value, id=key)
                dictionary[key] = s
                self._species.append(s)
            elif isinstance(value, (str)): # convert str to reaction
                r = reaction(value, id=key)
                if key != r.id:
                    if not r.id in dictionary:
                        dictionary[r.id] = r
#                    else:
#                        print 'Decided not to add reaction twice under name from string.'
                dictionary[key] = r
                self._reactions.append(r)
            elif isinstance(value, species):
                self._species.append(value)
            elif isinstance(value, reaction):
                self._reactions.append(value)
            elif isinstance(value, compartment):
                self._compartments.append(value)
        return super(metacompartment, self).__new__(self, name, bases, dictionary)

    @property
    def compartments(self):
        return self._compartments

    @property
    def reactions(self):
        return self._reactions

    @property
    def species(self):
        return self._species


class compartment(base): #@DuplicatedSignature
    __metaclass__ = metacompartment
#    import module_introspection.ply

    id_generator = compartment_id_generator

    def __init__(self, *args, **kwargs):
        self._species = self.__class__._species[:]
        self._reactions = self.__class__._reactions[:]
        self._compartments = self.__class__._compartments[:]
        for arg in args:
            if isinstance(arg, (species, compartment, reaction)):
                setattr(self, arg.id, arg)
            elif isinstance(arg, str):
                r = reaction(arg)
                setattr(self, r.id, r)
            else:
                raise ValueError('%s is not a species, compartment or reaction.' % arg)
        base.__init__(self, **kwargs)

    def __setattr__(self, name, value):
        ''' compartment().a = 1 and compartment(a=1) '''
        if name.startswith(reserved_attribute_name_prefixes):
            super(compartment, self).__setattr__(name, value)
            return
        if isinstance(value, (int, Quantity)):
            value = species(value, id=name)
            self._species.append(value)
        elif isinstance(value, (str)):
            value = reaction(value, id=name)
            self._reactions.append(value)
        elif isinstance(value, species):
            self._species.append(value)
        elif isinstance(value, reaction):
            self._reactions.append(value)
        elif isinstance(value, compartment):
            self._compartments.append(value)
        super(compartment, self).__setattr__(name, value)


    @property
    def compartments(self):
        return self._compartments

    @property
    def reactions(self):
        return self._reactions

    @property
    def species(self):
        return self._species


    @property
    def amounts(self):
        return dict([(s.name, s.amount) for s in self._species])

    def set_amounts(self, **kwargs):
        self.set_amounts()
        #TODO update species
        for id, amount in kwargs.items():
            pass

    def amount(self, id):
        return getattr(self, id, 0)

    def set_amount(self, id, amount):
        pass

#    def num_species(self):
#        return len(self.amounts)


    _volume = 1 * metre ** 3

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        if isinstance(volume, Quantity):
            try:
                volume.rescale('metre**3')
            except ValueError:
                raise ValueError('Dimensionality of volume (%s) cannot be rescaled to metre**3, required for concentration calculation.' % volume.dimensionality)
            if volume.size > 1:
                raise ValueError('...')
            self._volume = volume
        elif isinstance(volume, (int, float)):
            self._volume = volume * metre ** 3
        else:
            raise ValueError('Volume not a quantity, an int or a float: %s' % type(volume))

    def __getitem__(self, id):
        ''' compartment()[id] '''
        for i in itertools.chain(self.species, self.reactions, self.compartments):
#            don't
#            # descend into compartments
#            if isinstance(i, compartment):
#                item = i._get_item(id)
#                if item is not None:
#                    return item
            if i.id == id:
                return i

    def __setitem__(self, id, value):
        ''' compartment()[id] = value '''
        setattr(self, id, value)


#    def __str__(self):
#        return 'TODO'

    def __repr__(self):
        print ', '.join([str(i) for i in self.compartments])
        print ', '.join([str(i) for i in self.species])
        print ', '.join([str(i) for i in self.reactions])
#        return ', '.join(self.compartments + self.species + self.reactions)
        return 'TODO'







if __name__ == '__main__':
    c = compartment(# compartment *args can be species/compartment/reaction() or str but *not* int
        species(5), #, a), # no name or id should raise ValueError
        species(5, name='b'), #, a), # name but no id should use name as id - if there are no spaces?
        reaction('[ a ]_bacteria k-> [ b ]_bacteria k=0.1'), #, r1),
        'shit',
        reaction('rX: [ b ]_bacteria k-> [ a ]_bacteria k=0.01'), #, r2),
        compartment(
            compartment(a=1),
            a=2,
        ),
        a=3,
        b=1,
    )
    print c




#class subcompartment(compartment):
#    # coerced to species or reaction by metacompartment.__new__
#    a = 1
#    r1 = 'r2: signal [receptor ]_bacteria -K_D-> [signal_receptor]_media K_D = 0.001'
#    r2 = '[ ]_bacteria -k_production-> [signal_receptor]_media k_production = 0.001'
#
#
##print compartment.a.amount
##print compartment().a.amount
##print compartment(a=2).a.amount
#
##print compartment.species
##print compartment().species
##print compartment(b=2).species
###print compartment.r1
#
#c = subcompartment(name='name')
#print 'c.id', c.id
#print 'c.name', c.name
#c = subcompartment
#print c.id
#print c.reactions
#print c.r1
#print c.species
#print c.compartments

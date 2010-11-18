from types import GeneratorType
import itertools, re, sys
from id_generators import *
from infobiotics.commons.quantities.api import *
from infobiotics.commons.counter import Counter
from quantities import markup


class multiset(Counter):
    def __str__(self):
        ''' Returns 'a + b + b' for {'a':1,'b':2}. '''
        return ' + '.join([k for k, v in self.items() for _ in range(v)])


class base(object):
    ''' Base class for species, reaction and compartment that implements common functionality. 
    
    id should be automatically generated using self._id_generator.next(), too conform with SBML specification. 
    
    name should be a valid Python identifier that matches r"[_A-Za-z][_A-Za-z1-9]*" see http://homepage.mac.com/s_lott/books/python/html/p04/p04c04_re.html 
    
    '''

    @property
    def id(self):
        return self._id

    @property
    def metadata(self):
        return dict((k, v) for k, v in self.__dict__.items() if not k.startswith(('_', 'name'))) #TODO add to reversed prefixes?
    
    def __init__(self, **kwargs):
        if self.__class__.__name__ != 'base' and (not hasattr(self, '_id_generator') or not isinstance(self._id_generator, GeneratorType)):
            raise NotImplementedError("Subclasses of base must have a class attribute '_id_generator' that is a generator")

        # set id automatically
        self._id = self._id_generator.next() #FIXME use name_generator, abandon ids and make name readonly - use ids only for SBML, and name as id for IML. remove compartment base (add __getitem__ and reinstate properties in metacompartment and compartment that do different things)

        # set name if given and valid, falling back to id if not given and raising error if invalid
        name = kwargs.pop('name', None)
        if name is None:
            name = self.id
            self._named = False # used to distinguish model objects that are named explicitly as opposed to mirroring their generated id
        else:
            if not re.match('[_A-Za-z][_A-Za-z1-9]*', name):
                raise ValueError("name should be a valid Python identifier, i.e. a string that starts with a letter or _, and containing any number of letters, digits or _'s. Got '%s' " % name)
            self._named = True
        self.name = name
        
        # try and set all kwargs on instance
        for k, v in kwargs.items():
            setattr(self, k, v)
#            try:
#                setattr(self, k, v)
#            except AttributeError, e:
#                sys.stderr.write('base.__init__(%s=%s)\n' % (k, v if not isinstance(v, str) else "'%s'" % v))
#                raise e

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()
    
    def repr(self, indent=''):
        ''' Return indented string representation of object construction. '''
        raise NotImplementedError 

    def str(self, indent=''):
        ''' Return string representation of object. '''
        raise NotImplementedError

        
class species(base):
    _id_generator = species_id_generator

    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, amount):
        if isinstance(amount, int):
            self._amount = amount * molecules
            self._concentration = False
        elif isinstance(amount, Quantity):
            if amount.size > 1:
                raise ValueError('Species amounts should be single numbers, not arrays.')
            # quantity.rescale() raises ValueError if conversion not possible
            try:
                amount.rescale('mole')
                self._amount = amount
                self._concentration = False
            except ValueError:
                try:
                    amount.rescale('molar')
                    self._amount = amount
                    self._concentration = True
                except ValueError:
                    raise ValueError('Dimensionality of species amount (%s) not in molar, moles or molecules.' % amount.dimensionality)
        else:
            raise ValueError('Species amount must be an integer (number of molecules) or a quantity (in units of molecules, moles or molar concentration).')

    def __init__(self, amount=0 * molecule, name=None, **kwargs):
        self.amount = amount

        base.__init__(self, name=name, **kwargs)

    def str(self, indent=''):
        # adapted from Quantity.__str__
        if markup.config.use_unicode:
            dims = self.amount.dimensionality.unicode
        else:
            dims = self.amount.dimensionality.string
        if dims.startswith('molecule'):
#            return '%s = %d %s' % (self.id, self.amount.magnitude, dims)
#        return '%s = %s %s' % (self.id, str(self.amount.magnitude), dims)
#            return '%d %s %s' % (self.amount.magnitude, dims, self.name)
#        return '%s = %s %s' % (str(self.amount.magnitude), dims, self.name)
            return indent + "%d %s '%s'" % (self.amount.magnitude, dims, self.name)
        return indent + "%s = %s '%s'" % (str(self.amount.magnitude), dims, self.name)

    def repr(self, indent=''):
        return indent + "species(id='%s', name='%s', amount=%s * %s)" % (self.id, self.name, self.amount.magnitude, self.amount.dimensionality)
#        decl = '' if self._named else '%s=%s' % (self.id, self.__class__.__name__)
#        return indent + "%s%s * %s" % (decl, self.amount.magnitude, self.amount.dimensionality)


class reaction(base):
    _id_generator = reaction_id_generator

    rule_matcher = re.compile('\s*((?P<rule_id>\w+)\:)?\s*(?P<reactants_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<reactants_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<reactants_label>\w+)\s*-?(?P<rate_id>\w+)(->){1}\s*(?P<products_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<products_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<products_label>\w+)\s*(\w+)\s*\=\s*[-+]?(?P<rate>\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*')

    def __init__(self, reaction=None, **kwargs):

        self.rule_id = None
        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = 'l' #TODO compartment
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = 'l' #TODO compartment
        self.rate_id = 'k'
        self.rate = 0

        # overwrite above with kwargs
        base.__init__(self, **kwargs)

        if reaction is not None:
            if isinstance(reaction, str):
                # attempt regex
                match = self.rule_matcher.match(reaction)
                if match is not None:
                    match_groups_dict = match.groupdict()
                    for k, v in match_groups_dict.items():
                        if k == 'rule_id':
                            self.rule_id = v
                        elif k in ('reactants_outside', 'reactants_inside', 'products_outside', 'products_inside'):
                            if v is not None:
                                setattr(self, k, multiset([s.strip() for s in v.split('+')])) # can construct multiset from a list of str where the same str value might appear more than once
                            else:
                                setattr(self, k, multiset())
                        else:
                            setattr(self, k, v)
                else:
                    print 'Failed to create reaction from "%s"' % reaction

        #TODO rate - see infobiotics.commons.quantities.units.calculators:conversion_function_from_units

        #TODO needs testing
        if len(self.reactants_outside) > 2:
            raise ValueError("Rule '%s' has too many reactants outside, a maximum of 2 reactants is permitted for any reaction." % self.str())
        elif len(self.reactants_inside) > 2:
            raise ValueError("Rule '%s' has too many reactants inside %s, a maximum of 2 reactants is permitted for any reaction." % (self.str(), self.reactants_label))
        elif len(self.reactants_outside) + len(self.reactants_inside) > 2:
            raise ValueError("Rule '%s' has too many reactants, a maximum of 2 reactants is permitted for any reaction." % self.str())

        # must be after base.__init__ as id not set otherwise 
        if self.rule_id is not None:
            sys.stderr.write("Rule id '%s' of the rule '%s: %s' will not be used, instead the id '%s' will be used as it is guaranteed to be globally unique.\n" % (self.rule_id, self.rule_id, self.str(), self.id))

    def str(self, indent=''):
#        return indent + '%s: %s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s = %s' % (
#            self.id,
        return indent + '%s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s = %s' % (
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

    def repr(self, indent=''):
#        return indent + "reaction('%s')" % self.str()
        decl = '' if self._named else '%s=%s' % (self.id, self.__class__.__name__ if self.__class__.__name__ != 'species' else '')
        return indent + "'%s'" % self.str()



reserved_prefixes = ('_', 'species', 'reaction', 'compartment', 'amounts') # catches 'compartments' and 'reactions' properties too because of startswith

def self_dict_filtered_by_prefix_and_type(self, type):
    return dict((key, value) for key, value in dict((k, getattr(self, k)) for k in [i for i in dir(self) if not i.startswith(reserved_prefixes)]).items() if isinstance(value, type))

def self_dict_filtered_by_prefix_and_type_as_values_list(self, type):
    return self_dict_filtered_by_prefix_and_type(self, type).values()

class compartment(object): pass # forward declaration

class compartment_base(object):
    ''' Base class for compartment and metacompartment that implements common functionality. 
    
    Because we want compartment and metacompartment to behaviour similarly it makes sense to put almost everything here.
    
    '''
     
    @property
    def compartments(self):
#        return self_dict_filtered_by_prefix_and_type(self, compartment)
        return self_dict_filtered_by_prefix_and_type_as_values_list(self, compartment)

    @property
    def reactions(self):
#        return self_dict_filtered_by_prefix_and_type(self, reaction)
        return self_dict_filtered_by_prefix_and_type_as_values_list(self, reaction)

    @property
    def species(self):
#        return self_dict_filtered_by_prefix_and_type(self, species)
        return self_dict_filtered_by_prefix_and_type_as_values_list(self, species)

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

    @property
    def amounts(self):
        return dict([(s.name, s.amount) for s in self.species])

    def set_amounts(self, **kwargs): #TODO update species
        for id, amount in kwargs.items():
            pass

    def alphabet(self): pass #TODO


#    def __getitem__(self, name):
#        ''' Returns species amount, reaction rate or compartment attribute by matching name in that order. '''
#        for i in self.species:
#            if i.name == name:
#                return i.amount
#        for i in self.reactions:
#            if i.name == name:
#                return i.rate
#        return getattr(self, name)
#
#    def __setitem__(self, name, value):
#        ''' Quickly set species amount, reaction rate or compartment attribute by matching name in that order.'''
#        for i in self.species:
#            if i.name == name:
#                i.amount = value
#                return
#        for i in self.reactions:
#            if i.name == name:
#                i.rate = value
#                return
#        setattr(self, name, value)
#
    def __getitem__(self, id):
        ''' Returns species, reaction or compartment by matching id in that order, recursing into compartments. '''
        for i in itertools.chain(self.species, self.reactions, self.compartments):
            if i.id == id:
                return i
        # if that fails, descend into compartments
        for c in self.compartments:
            i = c[id]
            if i is not None:
                return i


reserved_attribute_name_prefixes = ('_', 'name', 'id', 'volume') # used by metacompartment.__new__ and compartment.__setattr__ 


class metacompartment(type, compartment_base):
    _id_generator = template_id_generator
    def __new__(self, name, bases, dictionary):
        ''' class c(compartment): a = 1, r1='...'
        
        Can directly alter dictionary. 
        
        Should be used for construction.
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        '''
        dictionary['id'] = self._id_generator.next()
        dictionary['name'] = name
        dictionary['bases'] = bases
        
        for key, value in dictionary.items():
            if key.startswith(reserved_attribute_name_prefixes):
                continue # deliberately skip the above keys
            if isinstance(value, (int, Quantity)): # convert int/Quantity to species #TODO float?
                s = species(value, name=key)
                dictionary[key] = s
            elif isinstance(value, (str)): # convert str to reaction
                r = reaction(value, name=key, reactants_label=name, products_label=name)
                dictionary[key] = r
            elif isinstance(value, (reaction)):
                print reaction.metadata #TODO
        return super(metacompartment, self).__new__(self, name, bases, dictionary)
    
    def __repr__(self):
        return 'class %s(%s):\n\t%s%s%s' % (
            self.name,
            ', '.join([base.__name__ for base in self.bases]),
            ',\n\t'.join([repr(i) for i in self.species]),
            ',\n\t'.join([repr(i) for i in self.reactions]),
            ',\n\t'.join([repr(i) for i in self.compartments]),
        )

#    def __str__(self):
#        return 'TODO'


class compartment(base, compartment_base): #@DuplicatedSignature
    __metaclass__ = metacompartment
    _id_generator = compartment_id_generator
#    import module_introspection.ply

    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, (species, compartment, reaction)):
                setattr(self, arg.name, arg)
            elif isinstance(arg, str):
                r = reaction(arg)
                setattr(self, r.name, r)
            else:
#                raise ValueError('%s is not a species, compartment or reaction.' % arg)
                sys.stderr.write("'%s' ignored.\n" % arg)
        base.__init__(self, **kwargs)

    def __setattr__(self, name, value):
        ''' compartment().a = 1 and compartment(a=1) '''
        if name.startswith(reserved_attribute_name_prefixes):
            super(compartment, self).__setattr__(name, value) # defer to properties
            return
        if isinstance(value, (int, Quantity)):
            value = species(value, name=name)
#        elif isinstance(value, float):
#            raise ValueError("Compartments don't know the meaning of floats like '%s', but they do understand ints (10) and quantities (0.5 * millimolar)." % name)
        elif isinstance(value, (str)):
            value = reaction(value, name=name, reactants_label=self.__class__.__name__, products_label=self.__class__.__name__)
        elif isinstance(value, (reaction)):
            print reaction.metadata #TODO
#            value = reaction(value, name=name, reactants_label=self.__class__.__name__, products_label=self.__class__.__name__)
        super(compartment, self).__setattr__(name, value)


    def repr(self, indent=''):
        decl = self.__class__.__name__ if self._named else '%s=%s' % (self.id, self.__class__.__name__)
        args = [i for i in self.species if i._named] + [i for i in self.reactions if i._named] + [i for i in self.compartments if i._named]
        kwargs = [i for i in self.species if not i._named] + [i for i in self.reactions if not i._named] + [i for i in self.compartments if not i._named]
        return '%s%s(\n%s%s%s%s%s)' % (
            indent,
            decl,
#            ',\n'.join([i.repr(indent + '\t') for i in self.species]),
#            ',\n' if len(self.species) > 0 else '',
#            ',\n'.join([i.repr(indent + '\t') for i in self.reactions]),
#            ',\n' if len(self.reactions) > 0 else '',
#            ',\n'.join([i.repr(indent + '\t') for i in self.compartments]),
#            ',\n' if len(self.compartments) > 0 else '',
            ',\n'.join([i.repr(indent + '\t') for i in args]),
            ',\n' if len(args) > 0 else '',
            ',\n'.join([i.repr(indent + '\t') for i in kwargs]),
            ',\n' if len(kwargs) > 0 else '',
            indent
        )
        
    def str(self, indent=''):
        return '%s%s(\n%s%s%s%s%s%s%s)' % (
            indent,
            self.id,
            '\n'.join([i.str(indent + '\t') for i in self.species]),
            '\n' if len(self.species) > 0 else '',
            '\n'.join([i.str(indent + '\t') for i in self.reactions]),
            '\n' if len(self.reactions) > 0 else '',
            '\n'.join([i.str(indent + '\t') for i in self.compartments]),
            '\n' if len(self.compartments) > 0 else '',
            indent
        ) 


if __name__ == '__main__':
    
#    # subclassing correctly *not replaces* but never creates a/s1 in d, only a/s2
#    class c(compartment):
#        a = 1
#    class d(c):
#        a = 2
#    print c.a, c.species, c['s1']
#    print d.a, d.species, d['s1']
    
    
##    # instantiating correctly replaces instance a/s1 with a/s2 without incorrect changing value of class species a/s1  
##    class c(compartment):
##        a = 1
###        a = species(1, 'test', desc='this is a test')
##    print 'c.a', c.a, c.species, c['s1']
##    d = c(a=2)
###    d = c(b=1)
##    print 'c.a', c.a, c.species, c['s1']
##    print 'd.a', d.a, d.species, d['s1']
##    assert c.a.amount == 1
##    print id(c.a)
##    print id(d.a)
##    assert d.a.amount == 2
    
#    # assigning new int to c.a updates existing species
#    c = compartment(a=1)
#    print c.a, c.species
#    c.a = 2
#    print c.a, c.species
#    
#    # assigning new int to c.a updates existing species
#    c = compartment(a=1)
#    print c.a, c.species
#    c.a = '[]_l k-> []_l k=1'
#    print c.a, c.species
    
    
    
    class c(compartment):
        a = 4
        r1 = '[ a ]_bacteria k-> [ b ]_bacteria k=0.1'
        r2 = reaction('[ a ]_bacteria k-> [ b ]_bacteria k=0.1')
    assert c[c.a.id].amount == 4 # c is class
    
    print c
    exit()

    c = compartment(# compartment *args can be species/compartment/reaction() or str but *not* int
        species(6), #, a), # no name or id should raise ValueError
        species(5, name='b'), #, a), # name but no id should use name as id - if there are no spaces?
        reaction('[ a ]_bacteria k-> [ b ]_bacteria k=0.1'), #, r1),
        reaction('rX: [ b ]_bacteria k-> [ a ]_bacteria k=0.01'), #, r2),
        compartment(
            compartment(a=1),
            a=2,
        ),
        a=3,
        b=1,
    )
    assert c[c.a.id].amount == 3 # c is instance
    print repr(c)
    print
    print c.species
    print c.reactions
    print c.compartments
    print c.amounts

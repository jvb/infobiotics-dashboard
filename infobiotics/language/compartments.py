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

    _named = False # used to distinguish model objects that are named explicitly as opposed to mirroring their generated id 
    
    def __init__(self, name=None, **kwargs):
        if self.__class__.__name__ != 'base' and (not hasattr(self, '_id_generator') or not isinstance(self._id_generator, GeneratorType)):
            raise NotImplementedError("Subclasses of base must have a class attribute '_id_generator' that is a generator")

        # set id automatically
        self.id = self._id_generator.next()
         
        # set name if given and valid, falling back to id if not given and raising error if invalid
        if name is not None:
            self._named = True
        else:
            name = self.id
        if not re.match('[_A-Za-z][_A-Za-z1-9]*', name):
            raise ValueError("name should be a valid Python identifier, i.e. a string that starts with a letter or _, and containing any number of letters, digits or _'s. Got '%s' " % name)
        self.name = name
        
        # try and set all kwargs on instance
        for k, v in kwargs.items():
            setattr(self, k, v)

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

    def __init__(self, amount=0 * molecule, name=None, **kwargs):
        if isinstance(amount, int):
            self.amount = amount * molecules
            self.is_concentration = False
        elif isinstance(amount, Quantity):
            if amount.size > 1:
                raise ValueError('Species amounts should be single numbers, not arrays.')
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
#        return indent + "species(id='%s', name='%s', amount=%s * %s)" % (self.id, self.name, self.amount.magnitude, self.amount.dimensionality)
        decl = '' if self._named else '%s=%s' % (self.id, self.__class__.__name__)
        return indent + "%s%s * %s" % (decl, self.amount.magnitude, self.amount.dimensionality)


class reaction(base):
    _id_generator = reaction_id_generator

    rule_matcher = re.compile('\s*((?P<rule_id>\w+)\:)?\s*(?P<reactants_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<reactants_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<reactants_label>\w+)\s*-?(?P<rate_id>\w+)(->){1}\s*(?P<products_outside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\[\s*(?P<products_inside>(\w+)\s*(\+\s*(\w+)\s*)*\s*)?\s*\]_(?P<products_label>\w+)\s*(\w+)\s*\=\s*[-+]?(?P<rate>\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*')

    def __init__(self, reaction_or_name=None, **kwargs):

        self.rule_id = None
        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = 'l' #TODO compartment
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = 'l' #TODO compartment
        self.rate_id = 'k'
        self.rate = 0

        if reaction_or_name is not None:
            if isinstance(reaction_or_name, str):
                # attempt regex
                match = self.rule_matcher.match(reaction_or_name)
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
                    reaction_or_name = None
                else:
                    print 'Failed to create reaction from "%s"' % reaction_or_name

        #TODO rate - see infobiotics.commons.quantities.units.calculators:conversion_function_from_units

        base.__init__(self, reaction_or_name, **kwargs)

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


class compartment_base(object):
    ''' Base class for compartment and metacompartment that implements common functionality. '''
     
    @property
    def compartments(self):
        return self._compartments

    @property
    def reactions(self):
        return self._reactions

    @property
    def species(self):
        return self._species
    
    def __getitem__(self, name):
        for i in itertools.chain(self.species, self.reactions, self.compartments):
#            don't
#            # descend into compartments
#            if isinstance(i, compartment):
#                item = i._get_item(id)
#                if item is not None:
#                    return item
            if i.name == name:
                return i

    def __setitem__(self, name, value):
        setattr(self, name, value)
#        for i in itertools.chain(self.species, self.reactions, self.compartments):
#            if i.name == name:
#                setattr(self, name, value)
#                return


reserved_attribute_name_prefixes = ('_', 'name', 'id', 'volume')


class compartment(object): pass # forward declaration needed in metacompartment.__new__ switch


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
        
        self._species = []
        self._reactions = []
        self._compartments = []
        
        for key, value in dictionary.items():
            
            if key.startswith(reserved_attribute_name_prefixes):
                continue #TODO why not raise an Error?
            
            if isinstance(value, (int, Quantity)): # convert int/Quantity to species #TODO float?
                s = species(value, name=key)
                dictionary[key] = s
                self._species.append(s)
            
            elif isinstance(value, (str)): # convert str to reaction
                r = reaction(value, name=key)
                dictionary[key] = r
                self._reactions.append(r)
            
            elif isinstance(value, species):
                self._species.append(value)
            
            elif isinstance(value, reaction):
                self._reactions.append(value)
            
            elif isinstance(value, compartment):
                self._compartments.append(value)
        
        return super(metacompartment, self).__new__(self, name, bases, dictionary)


class compartment(base, compartment_base): #@DuplicatedSignature
    __metaclass__ = metacompartment
#    import module_introspection.ply

    _id_generator = compartment_id_generator

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
        if isinstance(value, float):
            raise ValueError("Compartments don't know the meaning of floats like '%s', but they do understand ints and quantities." % name)
        elif isinstance(value, (int, Quantity)): #TODO float?
#            
#            # if a species with id == name exists in class then update amount of species with value in self
#            
#            # elif another object with id == name exists in class then raise Error?
#            
#            
#            d = dict(self.__class__.__dict__) # copy items from class dictproxy
#            d.update(self.__dict__) # overwrite traits with instances from self
##            d.update(self.__dir_items()) # catches attributes of superclasses
#            print 'got here'
#            try:
#                s = d[name]
#                if isinstance(s, species):
#                    s.amount = value
#            except KeyError:
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

#    def _setattr(self, name, value): pass #TODO use to make if, elif switch consistent for compartment and metacompartment

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
    
    class c(compartment):
        a = 4
    assert c['a'] == 4 # c is class

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
    print repr(c)
#    assert c['a'] == 3 # c is instance



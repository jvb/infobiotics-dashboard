__all__ = ['compartment']

from core import named, Quantity
from enthought.traits.api import Either, Instance, List, Tuple, Dict, Str, Int, Float, Any, Property
import itertools
from species import species
from reaction import reaction
from id_generators import *

CompartmentOrSpeciesOrReactions = Either(

    # compartments
    Instance('compartment'),
    List(Instance('compartment')),
    Tuple(Instance('compartment')),

    # species
    Int, Quantity, #TODO a=10, a=10*M, a=10*molecules
    Instance('species'),
    List(Instance('species')),
    Tuple(Instance('species')),
#    Dict(Str, Int), # initial_amounts = {'a':1} THIS IS FORBIDDEN because it leads to ambiguity - overwriting explicitly named amounts with dict mappings. Can use compartment(**amounts) instead 
#    ListStr, Tuple(Str) #TODO alphabet?

    # reactions
#    Str, #TODO regex for r1: a + b [c + d ]_l -k_on-> e + f[  g + h]_j k_on   =     0.01
    Instance('reaction'),
    List(Instance('reaction')), # id's assigned from reaction_id_generator# id's assigned from reaction_id_generator
#    List(List(Instance('Reaction'))), # ditto
#    List(Tuple(Instance('Reaction'))), # ditto
    Tuple(Instance('reaction')), # ditto
#    Tuple(List(Instance('Reaction'))), # ditto
#    Tuple(Tuple(Instance('Reaction'))), # ditto
    Dict(Str, Instance('reaction')), # id's assigned from dict keys for instance in modules 
)


# factoring out __getattribute__ and __setattr__ from metacompartment and compartment

basic_types = (int, dict) # types that can be converted into model objects

def __getattribute__(self, name, parent):
    ''' Convert basic types on first access if they were set at class 
    declaration time using __setattr__. Doesn't convert private traits. '''
    value = parent.__getattribute__(name)
    if not name.startswith(('_', 'wrappers')) and isinstance(value, basic_types):
#        print '%s.__getattribute__' % self
        __setattr__(self, name, value, parent) # convert value to object via __setattr__
        return parent.__getattribute__(name)
    return value

def __setattr__(self, name, value, parent):
    ''' Convert basic types on assignment. Doesn't convert private traits. '''
#    print '%s.__setattr__(%s, %s)' % (self, name, value)
    if not name.startswith(('_', 'wrappers')) and isinstance(value, basic_types):
        if isinstance(value, int): # convert int to species
            parent.__setattr__(name, species(value, id=name))
#        elif isinstance(value, dict):
#    #        print '%s.__setattr__' % self
#            for k, v in value.items():
#                if not (isinstance(k, str) and isinstance(v, int)):
#                    raise ValueError
#                __setattr__(self, k, v, parent)
        else:
            print name, value#, parent
    else:
        parent.__setattr__(name, value)


def dict_sorted_by_key(dictionary):
    return ', '.join(['%s=%s' % (key, dictionary[key]) for key in sorted(dictionary.keys())])

from enthought.traits.api import MetaHasTraits

class metacompartment(MetaHasTraits):
    ''' Needed to convert class attributes to correct types. See: 
    http://docs.python.org/reference/datamodel.html#special-method-lookup-for-new-style-classes 
    
    '''

    def __new__(self, name, bases, dictionary):
        ''' Should be used for construction. 
        
        Can directly alter dictionary. 
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        '''
#        print type(self), dict_sorted_by_key(dictionary)
##        dictionary['a'] = 1 # adds a=1

        parent = super(metacompartment, self)
        return parent.__new__(self, name, bases, dictionary)


    def __init__(self, name, bases, dictionary):
        ''' Should be used for verification or registration. 
        
        Maybe better to convert species here than overwrite getattribute, etc
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        '''
#        print type(self), dict_sorted_by_key(dictionary)
##        dictionary['a'] = 2 # does nothing

        #TODO dicts are unordered so we can't be sure which definition was last
        #TODO therefore a = 1 and b = {'a':2} could results in a == 1 or a == 2  
        parent = super(metacompartment, self)
#        for k, v in dict(dictionary).items():
#            if not k.startswith('_') and isinstance(v, basic_types):
#                if k == 'a' or k == 'b':
#                    print v
#                __setattr__(self, k, v, parent) #TODO what about b = {'b':1}? 
#        parent.__init__(name, bases, self.__dict__)
        parent.__init__(name, bases, dictionary)

#    def __getattribute__(self, name):
#        ''' compartment.name '''
#        return __getattribute__(self, name, super(metacompartment, self))
#
#    def __getattr__(self, name):
#        ''' compartment.name when name not in self.__dict__ '''
#
#    def __setattr__(self, name, value):
#        ''' compartment.name = value '''
#        __setattr__(self, name, value, super(metacompartment, self))
#
#    def __getitem__(self, name):
#        ''' compartment[name] '''
#
#    def __setitem__(self, name, value):
#        ''' compartment[name] = value '''

#    def __str__(self):
#        return 'Yeah baby, wooh!'


class compartment(named):
    __metaclass__ = metacompartment

    volume = Float #TODO make into a litre/length**3 validated Trait
    __ = Any
    _ = CompartmentOrSpeciesOrReactions

#    def __str__(self):
#        return 'Oh no!'

#    def __getattribute__(self, name):
#        ''' compartment().name 
#        
#        Spy on attribute access, sending basic types for conversion. 
#
#        Used because HasTraits doesn't define __getattr__. See: 
#        http://docs.python.org/reference/datamodel.html#object.__getattribute__
#        
#        '''
#        return __getattribute__(self, name, super(compartment, self))
#
#    def __getattr__(self, name):
#        ''' compartment().name when name not in self.__dict__ '''
#
#    def __setattr__(self, name, value):
#        ''' compartment().name = value 
#        
#        Spy on attribute assignment and convert basic types. 
#        
#        '''
#        __setattr__(self, name, value, super(compartment, self))
#
#    def __getitem__(self, id):
#        ''' compartment()[name] 
#        
#        Enable mapping item access, e.g. compartment[id]
#        
#        '''
#        for i in itertools.chain(self.species, self.reactions, self.compartments):
##            don't
##            # descend into compartments
##            if isinstance(i, compartment):
##                item = i._get_item(id)
##                if item is not None:
##                    return item
#            if i.id == id:
#                return i
#
#    def __setitem__(self, id, value):
#        ''' Enable mapping item assignment, e.g. compartment[id] = subcompartment '''
#        setattr(self, id, value)

##    def __class_dir(self):
##        return [name for name in dir(self.__class__) if not name.startswith(('__', '_')) and not callable(getattr(self.__class__, name)) and name != 'wrappers']
#
##    def __class_dir_items(self):
##        return dict([(name, getattr(self.__class__, name)) for name in self.__class_dir()])

    def __dir(self):
        return [name for name in dir(self) if not name.startswith('_') and not callable(getattr(self, name)) and name != 'wrappers']

    def __dir_items(self):
        return dict([(name, getattr(self, name)) for name in self.__dir()])
#
    def __attributes(self, type):
        d = dict(self.__class__.__dict__) # copy items from class dictproxy
        d.update(self.__dict__) # overwrite traits with instances from self
        d.update(self.__dir_items()) # catches attributes of superclasses
        return filter_by_type(d, type)
#
##    def __instance_attributes(self, type):
##        d = dict(self.__dict__)
###        d.update(self.__dir_items())
##        return filter_by_type(d, type)
##    def _instance_compartments(self):
##        return self.__instance_attributes(compartment)
##    def _instance_species(self):
##        return self.__instance_attributes(species)
##    def _instance_reactions(self):
##        return self.__instance_attributes(reaction)
#
##    def __class_attributes(self, type):
##        d = dict(self.__class__.__dict__)
##        d.update(self.__dir_items())#d.update(self.__class_dir_items())
##        return filter_by_type(dict(d), type)
##    def _class_compartments(self):
##        return self.__class_attributes(compartment)
##    def _class_species(self):
##        return self.__class_attributes(species)
##    def _class_reactions(self):
##        return self.__class_attributes(reaction)
#
    compartments = Property(List(Instance('compartment')))
    def _get_compartments(self):
        return self.__attributes(compartment)

    species = Property(List(Instance('species')))
    def _get_species(self):
#        #TODO self.__attributes(int)
#        # self.__attributes(dict)
#        ld = self.__attributes(dict)
#        ld = [d for d in ld if isinstance(d.items()[0][0], str) and isinstance(d.items()[0][1], int)]
##        print ld
        return self.__attributes(species)

    reactions = Property(List(Instance('reaction')))
    def _get_reactions(self):
        return self.__attributes(reaction)

##    def amount(self, id):
##        i = self[id]
##        if i is None or not isinstance(i, species):
##            raise ValueError('%s is not a species' % id)
##        return i.quantity
#    amounts = Property(Dict(Str, Int))
#    def _get_amounts(self):
#        return dict([(s.name, s.amount) for s in self.species])
#    def _set_amounts(self): #TODO
#        pass

    @property
    def amounts(self):
        return dict([(s.name, s.amount) for s in self.species])
    @amounts.setter
    def set_amounts(self):
        print 'got here'

    def num_species(self):
        return len(self.amounts)

    def __init__(self, **kwargs):
        for k, v in kwargs:
            setattr(self, k, v)


def filter_by_type(d, type):
    ''' Used to extract attributes by type and to create traits from class 
    attributes... '''
    filtered = []

    def fix_missing_id(item, id):
        if hasattr(item, 'id') and item.id == '':
            item.id = id

    def append_item(item, id):
        ''' Recursive so that it can work with nested sequences. '''
        #TODO add int -> species here?
        if isinstance(item, type):
            fix_missing_id(item, id)
            filtered.append(item)
        elif hasattr(item, '__iter__'):
            if isinstance(item, dict):
                for k, v in item.items():
                    append_item(v, k)
            else:
                for i in item:
                    append_item(i, globals()['%s_id_generator' % type.__name__].next())

    for id, item in d.items():
        if id.startswith('_'): continue # skip private keys #TODO necessary now that __dir does this?
        append_item(item, id)

    return filtered



if __name__ == '__main__':

#    # test __str__
#    print compartment # metacompartment.__str__
#    print compartment() # compartment.__str__

#    # test __repr__
#    print repr(compartment) # metacompartment.__repr__
#    print repr(compartment()) # compartment.__repr__

    class C(compartment):
#        __metaclass__ = metacompartment
        a = 1
#        b = {'a':5}
#
#    class D(C):
#        a = 2
#
    print type(C.a)
#    print D.a

    c = C()
    print type(c.a)
    c.a = 2

    print c.amounts

#    amounts = {'e':20, 'f':10}
#    c = compartment(a=3, b=4, c=5, d=0, **amounts)
#    print c.a, c.b, c.c, c.d, c.e, c.f
#    print c.species
#    print c.amounts
#
##    c = C()
###        print C.a, type(C.a)
###        print c.a, type(c.a)
###        print c.b
##    print C.a, c.a, c.b, c.a
###        C.a = 6
###        print c.a
###        print C().a

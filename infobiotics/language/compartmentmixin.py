from infobiotics.commons.descriptors import mixedmethod
from infobiotics.commons.sequences import flatten, iterable
from infobiotics.commons.quantities import *
from species import species
from reactions import reaction
from config import repr
import itertools
compartment = None # patched by compartments module later 

reserved_prefixes = (
    '_', # prefix for hidden variables
    'reserved_prefixes', # this 
    'reserved_attribute_name_prefixes', # attribute of compartmentmixin, used by metacompartment.__new__ and compartment.__setattr__ 
    'outside', # prevent recursion when print metadata as outer compartment of inner compartment has a reference inner compartment ...
    # properties/methods
    'species',
    'reaction', # catches 'reactions' too because of startswith
    'compartment', # catches 'compartments' too because of startswith
    'metadata',
    'amounts',
)

#def dir_dict(o):
#    return dict((name, getattr(o, name)) for name in dir(o))
#
#def dir_dict_filtered_by_prefix(o, *prefixes):
#    return dict((name, value) for name, value in dir_dict(o).items() if not name.startswith(prefixes))
#
#def dir_dict_filtered_by_type(o, *types):
#    return dict((name, value) for name, value in dir_dict(o).items() if isinstance(value, types))
#
#def dir_dict_filtered_by_prefix_and_type(o, prefixes, types):
#    return dict((name, value) for name, value in dir_dict(o).items() if not name.startswith(prefixes) and isinstance(value, types))
#
#print dir_dict('s')
#print dir_dict_filtered_by_prefix('s', '_', 'up')
#exit()

def dir_filtered_by_prefix_and_type(c, type):
    ''' Uses dir(c) to obtain a list of valid attributes for that 
    compartment from its instance and class, thereby allowing species, 
    reactions and compartments to be inherited. See: 
    http://docs.python.org/library/functions.html#dir
    
    Skips attributes with names in reserved_prefixes.
    
    '''
    return dict(
        (key, value) for key, value in dict(
            (k, getattr(c, k)) for k in [i for i in dir(c) if not i.startswith(reserved_prefixes)]
        ).items() if isinstance(value, type)
    )


from types import FunctionType, MethodType

class _SimpleTest:
    ''' from enthought.traits.has_traits '''
    def __init__(self, value): self.value = value
    def __call__(self, test): return test == self.value

def filter_dict_by_metadata(dictionary, **metadata):
    ''' Adapted from enthought.traits.has_traits.HasTraits.traits(self, **metadata) '''
    if len(metadata) == 0: # nothing to do
        return dictionary
    # make attributes named in metadata callable by wrapping in _SimpleTest
    for meta_name, meta_eval in metadata.items():
        if type(meta_eval) is not FunctionType:
            metadata[meta_name] = _SimpleTest(meta_eval)
    result = {}
    for key, value in dictionary.items(): # for each named item
        for meta_name, meta_eval in metadata.items(): # for all metadata
            if not hasattr(value, meta_name): # check for metadata attribute on item
                break # break inner for loop because metadata attribite not found
            if not meta_eval(getattr(value, meta_name)): # call meta_eval with item.meta_name
                break # break inner for loop because some metadata didn't match
        else: # all metadata matched
            result[key] = value
    return result

def filter_list_by_metadata(l, **metadata):
    ''' Adapted from filter_dictionary_by_metadata to work with lists because
    the same name might be shared by multiple compartments and reactions.  '''
    if len(metadata) == 0: # nothing to do
        return l
    # make attributes named in metadata callable by wrapping in _SimpleTest
    for meta_name, meta_eval in metadata.items():
        if type(meta_eval) is not FunctionType:
            metadata[meta_name] = _SimpleTest(meta_eval)
    result = []
    for item in l: # for each named species
        for meta_name, meta_eval in metadata.items(): # for all metadata
            if not hasattr(item, meta_name): # check for metadata attribute on item
                break # break inner for loop because metadata attribite not found
            if not meta_eval(getattr(item, meta_name)): # call meta_eval with item.meta_name
                break # break inner for loop because some metadata didn't match
        else: # all metadata matched
            result.append(item)
    return result


class filterablelist(list):
    ''' A list which can be filtered by metadata of the objects it contains 
    when called with a dictionary of metadata criteria. Doesn't work for int, 
    etc. 
    
    Used by compartmentmixin to provide readonly properties whose results are 
    filterable. For example compartment().species returns a list of species.
    compartment().species(name='a') returns a list of species whose name is 'a'. 
    '''
    def __call__(self, **metadata):
        ''' See filter_list_by_metadata.
        
            >>> class o(object):
            ...     def __init__(self, value):
            ...         self.value = value
            >>> l = filterablelist([o(1), o(2), o(3)])
            >>> len(l(value=lambda x: x >= 2))
            2

        '''
        return filterablelist(filter_list_by_metadata(self, **metadata))

    def __add__(self, other):
        '''
        >>> filterablelist(['a']) + ['b']
        filterablelist(['a','b'])
        '''
        return filterablelist(list.__add__(self, other))

    def __radd__(self, other):
        '''
        >>> ['b'] + filterablelist(['a'])
        filterablelist(['b','a'])
        '''
        return filterablelist(list.__add__(other, self))

    def __iadd__(self, other):
        return self.extend(other) # seemingly uses __radd__ and so returns a filterablelist

class filterabledict(dict):
    def __call__(self, **metadata):
        return filter_dict_by_metadata(self, **metadata)

def _getter(compartmentmixin, type):
    ''' Returns a filterablelist of objects of type 'type' from the 
    values of the compartment's attributes.
    
    Previously and removed duplicates using a set because it could make 
    sense to instantiate a class and use it several times? e.g. same as 
    a ToolkitEditorFactory like TableEditor in Traits. 
    
    '''
    # single objects of type 'type' 
    d = dir_filtered_by_prefix_and_type(compartmentmixin, type)
    l = d.values()
    # sequences, possibly nested, possibly containing objects of type 'type'
    d = dir_filtered_by_prefix_and_type(compartmentmixin, (list, tuple))
    for value in d.values():
        [l.append(i) for i in flatten(value) if isinstance(i, type)]
#    s = set(l)
#    return filterablelist(s)
    return filterablelist(l)

class compartmentmixin(object):
    ''' Mixin for compartment and metacompartment that implements common
    functionality. 
    
    Because we want compartment and metacompartment to behaviour similarly it
    makes sense to put almost everything here.
    
    **metadata in some of the property getters is just there as a placeholder
    for the API. Its value will always be an empty dict and that shouldn't
    get passed on. The object (probably a list) that is returned gets called
    immediately with the metadata kwargs/dictionary from wherever this property 
    was accessed.

    '''

    reserved_attribute_name_prefixes = ('_', 'volume', 'outside', 'label') # used by metacompartment.__new__ and compartment.__setattr__


    @property
    def compartments(self, **metadata): #@UnusedVariable
        ''' Returns a list of all the compartments in the compartment that match the 
        set of *metadata* criteria. '''
        return _getter(self, compartment)

    @property
    def reactions(self, **metadata): #@UnusedVariable
        ''' Returns a list of all the reactions in the compartment that match the 
        set of *metadata* criteria. '''
        return _getter(self, reaction)

    @property
    def species(self, **metadata): #@UnusedVariable
        ''' Returns a list of all the species in the compartment that match the 
        set of *metadata* criteria. 
        
        For example, to get all species with amounts > 5:

            >>> from infobiotics.language.compartments import compartment
            >>> c = compartment(a=5,b=6,c=7)
            >>> len(c.species(amount=lambda x: x > 5))
            2

        '''
        return _getter(self, species)


    @property
    def metadata(self):
        return dict(
            (key, value) for key, value in dict(
                (k, getattr(self, k)) for k in [i for i in dir(self) if not i.startswith(reserved_prefixes)]
            ).items() if not isinstance(value, (species, reaction,
                                                compartmentmixin, # covers metacompartment and compartment 
                                                MethodType, # hide methods and thereby prevent infinite recursion
                                                FunctionType, # hide functions ( and methods decorated with @mixedmethod)
                                                ))
        )


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
                raise ValueError('Volume should be a single value, not an array.')
            self._volume = volume
        elif isinstance(volume, (int, float)):
            self._volume = volume * metre ** 3
        else:
            raise ValueError('Volume not a quantity, an int or a float: %s' % type(volume))


#    @property
#    def amounts(self):
#        ''' Readonly property that returns a dictionary of the amounts of all species. '''
#        return dict([(s.name, s.amount) for s in self.species])
    def amounts(self, **metadata):
        ''' Method that returns a dictionary of the amount of all species matching the metadata criteria. '''
        l = self.species(**metadata)
        return dict([(s.name, s.amount) for s in l])
#        return filterabledict(...) #TODO make property and return filterabledict

    def set_amounts(self, **kwargs): #TODO update species
        species = dir_filtered_by_prefix_and_type(self, species).values()
        for name, amount in kwargs.items():
            s = species[name]
            if s is None:
                pass # create new species
#            elif # TODO is it possible test if s belong to class rather than instance? 


    def alphabet(self): pass #TODO


##    def __getitem__(self, name):
##        ''' Returns species amount, reaction rate or compartment attribute by matching name in that order. '''
##        for i in self.species:
##            if i.name == name:
##                return i.amount
##        for i in self.reactions:
##            if i.name == name:
##                return i.rate
##        return getattr(self, name)
##
##    def __setitem__(self, name, value):
##        ''' Quickly set species amount, reaction rate or compartment attribute by matching name in that order.'''
##        for i in self.species:
##            if i.name == name:
##                i.amount = value
##                return
##        for i in self.reactions:
##            if i.name == name:
##                i.rate = value
##                return
##        setattr(self, name, value)
##
#    def __getitem__(self, id):
#        ''' Returns species, reaction or compartment by matching id in that order, recursing into compartments. '''
#        for i in itertools.chain(self.species, self.reactions, self.compartments):
#            if i.id == id:
#                return i
#        # if that fails, descend into compartments
#        for c in self.compartments:
#            i = c[id]
#            if i is not None:
#                return i


#    def __str__(self):
#        return self.str()
#    
#    def __repr__(self):
#        return self.repr()

    @mixedmethod
    def repr(self, indent='\t', indent_level=0, id='', evalable=True):
        ''' Returns an evalable string. 
        
        Warning: some quantities use symbols which are likely to be overridden
        in the eval statements context (locals() and globals()). For example
        a quantity like 1 metre**3 returns a repr() string of 'array(1) * m**3'.
        A global variable named 'm' that is not an alias for metre will raise a
        "TypeError: unsupported operand type(s) for ** or pow(): 'list' and 'int'."

        Warning: metaclass...

        '''
        metadata = self.metadata
        def get_metadata_strs(indent=indent, indent_level=indent_level + 1, as_dict_items=False):
            _metadata = []
            assignment = ':' if as_dict_items else '='
            for k, v in metadata.items():
                e = '%s%s%s' % (indent * indent_level, "'%s'" % k if as_dict_items else k, assignment) # assignment to k
                if iterable(v):
                    s = '%s%s%s[\n' % (indent * indent_level, "'%s'" % k if as_dict_items else k, assignment)
                    for i in flatten(v): # flatten iterables because that is how compartment.add treats them and we get full info
                        s += '%s,\n' % (i.repr(indent, indent_level + 1) if hasattr(i, 'repr') else (indent * (indent_level + 1)) + repr(i))
                    s += indent + ']'
                    _metadata.append(s)
                elif isinstance(v, basestring):
                    if k == 'label' and not self._explicitly_labelled:#((isinstance(self, type) and v == self.__name__)or (v == self.__class__.__name__)): # hide label when repr(class) or repr(instance) when same as default
                        continue
                    _metadata.append(e + "'%s'" % v)
                else:
                    if k == 'volume':
                        if v == compartment.volume: # hide volume when same as default
                            continue
                        else:
                            pass #TODO?
#                    # done in reserved_prefixes
#                    if k == 'outer':
#                        continue
                    _metadata.append(e + repr(v))
            return _metadata
        metadata_strs = get_metadata_strs()

        # named
        compartments = dir_filtered_by_prefix_and_type(self, compartment) # don't panic, compartment is set on compartmentmixin by compartments module
        reactions = dir_filtered_by_prefix_and_type(self, reaction)
        from species import species as species_ # fixes UnboundLocalError: local variable 'species' referenced before assignment
        species = dir_filtered_by_prefix_and_type(self, species_)

        # switch depending on whether method called with class or instance        
        if isinstance(self, type): # class
            if evalable:
                return "type('%s', (%s%s), {%s%s%s})" % (
                    self.__name__,
#                    ', '.join([base.__name__ for base in self._bases]),
                    ', '.join([base.repr() if base.__name__ != 'compartment' else 'compartment' for base in self._bases]),
                    ',' if len(self._bases) == 1 else '',
                    ', '.join(["'%s':%s" % (k, v.repr()) for k, v in itertools.chain(compartments.items(), reactions.items(), species.items())]),
                    ', ' if len(metadata_strs) > 0 else '',
                    ', '.join(get_metadata_strs(as_dict_items=True))
                )
            else:
                return '%sclass %s(%s):%s\n%s%s%s%s%s%s%s%s%s' % (
                    indent * indent_level,
                    self.__name__,
                    ', '.join([base.__name__ for base in self._bases]),
                    ' pass' if len(compartments) + len(reactions) + len(species) + len(metadata_strs) == 0 else '',
                    '\n'.join([i.repr(indent, indent_level + 1, k) for k, i in compartments.items()]),
                    '\n' if len(compartments) > 0 else '',
                    '\n'.join([i.repr(indent, indent_level + 1, k) for k, i in reactions.items()]),
                    '\n' if len(reactions) > 0 else '',
                    '\n'.join([i.repr(indent, indent_level + 1, k) for k, i in species.items()]),
                    '\n' if len(species) > 0 else '',
                    '\n'.join(metadata_strs), #indent, indent_level+1
                    '\n' if len(metadata_strs) > 0 else '',
                    indent * indent_level,
                )

        else: # instance

            # anonymous (only in instance)
            _compartments = self._compartments if hasattr(self, '_compartments') else []
            _reactions = self._reactions if hasattr(self, '_reactions') else []
            _species = self._species if hasattr(self, '_species') else []

            len_contents = len(_compartments + _reactions + _species + compartments.items() + reactions.items() + species.items() + metadata_strs)

            return '%s%s%s%s(%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s)' % (#%s
                indent * indent_level,
                id,
                '=' if id != '' else '',
                self.__class__.__name__,
                '\n' if len_contents > 0 else '',
                ',\n'.join([i.repr(indent, indent_level + 1) for i in _compartments]),
                ',\n' if len(_compartments) > 0 else '',
                ',\n'.join([i.repr(indent, indent_level + 1) for i in _reactions]),
                ',\n' if len(_reactions) > 0 else '',
                ',\n'.join([i.repr(indent, indent_level + 1) for i in _species]),
                ',\n' if len(_species) > 0 else '',
                ',\n'.join([i.repr(indent, indent_level + 1, k) for k, i in compartments.items()]),
                ',\n' if len(compartments) > 0 else '',
                ',\n'.join([i.repr(indent, indent_level + 1, k) for k, i in reactions.items()]),
                ',\n' if len(reactions) > 0 else '',
                ',\n'.join([i.repr(indent, indent_level + 1, k) for k, i in species.items()]),
                ',\n' if len(species) > 0 else '',
                ',\n'.join(metadata_strs), #indent, indent_level+1
                ',\n' if len(metadata_strs) > 0 else '',
                indent * indent_level if len_contents > 0 else '',
            )

    @mixedmethod
    def str(self, indent='\t', indent_level=0, id='', evalable=False):
#        if isinstance(self, type):
#            pass
#        else:
#            pass
        return self.repr(indent, indent_level, id, evalable)


if __name__ == '__main__':
    execfile('module1.py')

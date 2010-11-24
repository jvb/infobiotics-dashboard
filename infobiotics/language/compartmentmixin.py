from infobiotics.commons.sequences import flatten, iterable
from infobiotics.commons.quantities.api import metre
import itertools
from species import species
from reactions import reaction

reserved_prefixes = ('reserved_prefixes', 'reserved_attribute_name_prefixes', 'metadata', '_', 'name', 'species', 'reaction', 'compartment', 'amounts') # catches 'compartments' and 'reactions' properties too because of startswith

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
        return filter_list_by_metadata(self, **metadata)

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

    reserved_attribute_name_prefixes = ('_', 'name', 'id', 'volume', 'outside', 'label') # used by metacompartment.__new__ and compartment.__setattr__


    @property
    def compartments(self, **metadata):
        ''' Returns a list of all the compartments in the compartment that match the 
        set of *metadata* criteria. '''
        return _getter(self, compartment)

    @property
    def reactions(self, **metadata):
        ''' Returns a list of all the reactions in the compartment that match the 
        set of *metadata* criteria. '''
        return _getter(self, reaction)

    @property
    def species(self, **metadata):
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
            ).items() if not isinstance(value, (species, compartmentmixin, reaction, MethodType))
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
                raise ValueError('...')
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
        return dict([(s.name, s.amount) for s in self.species(**metadata)])

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


    def __str__(self):
        return self.str()

    def str(self, indent=''):
        return '%s%s(\n%s%s%s%s%s%s%s)' % (
            indent,
            self.label,
            '\n'.join([i.str(indent + '\t') for i in self.species]),
            '\n' if len(self.species) > 0 else '',
            '\n'.join([i.str(indent + '\t') for i in self.reactions]),
            '\n' if len(self.reactions) > 0 else '',
            '\n'.join([i.str(indent + '\t') for i in self.compartments]),
            '\n' if len(self.compartments) > 0 else '',
            indent
        )


#    def repr(self, indent=''):
#        return 'class %s(%s):\n\t%s%s%s' % (
#            self.name,
#            ', '.join([base.__name__ for base in self.bases]),
#            ',\n\t'.join([repr(i) for i in self.species]),
#            ',\n\t'.join([repr(i) for i in self.reactions]),
#            ',\n\t'.join([repr(i) for i in self.compartments]),
#        )
#
#
    def __repr__(self):
        return self.repr()

    def repr(self, indent='', id=''):
        from species import species

        # list/tuple
#        sequences = dir_filtered_by_prefix_and_type(self, (list, tuple))
        #TODO reduce each named sequence get compartments, reactions and species
#        [flatten(value) for value in dir_filtered_by_prefix_and_type(self, (list, tuple)).values()]
#        print sequences
#        [i for i in sequences if isinstance(i, compartment)]
#        [i for i in sequences if isinstance(i, reaction)]
#        [i for i in sequences if isinstance(i, species)]

        # or use metadata?
        metadata = self.metadata
        def metadata_str(indent=''):
            '''
            
            compartment(
                s = [
                    1,
                    2,
                ]
                t = 5,
                v = 'six',
                
            
            '''
            _metadata = []
            for k, v in metadata.items():
                e = '%s=' % k
#                '%s=[%s]' % (k, ',\n'.join([i.__repr__() for i in v if hasattr(i, 'repr') for k, v in metadata.items()])) if iterable(v) else '%s=%r' % (k, v)
                if iterable(v):
                    s = '%s=[\n' % k
                    for i in v:
                        s += '\t%r,\n' % i
                    s += '],\n'
                    _metadata.append(s)
                elif isinstance(v, basestring):
                    print self.__class__.__name__ #TODO continue from here
                    if k == 'label' and v == self.__class__.__name__:
                        continue
                    _metadata.append(e + "'%s'" % v)
                else:
                    _metadata.append(e + str(v))
            return ',\n'.join(_metadata)

#        metadata_str('\t')
        print metadata_str('\t')
        exit()



        # named
        compartments = dir_filtered_by_prefix_and_type(self, compartment)
        reactions = dir_filtered_by_prefix_and_type(self, reaction)
        species = dir_filtered_by_prefix_and_type(self, species)

        # anonymous
        _compartments = self._compartments if hasattr(self, '_compartments') else []
        _reactions = self._reactions if hasattr(self, '_reactions') else []
        _species = self._species if hasattr(self, '_species') else []

        return '%s%s%s%s(\n%s%s%s%s%s%s%s%s%s%s%s%s%s)' % (
            indent,
            id,
            '=' if id != '' else '',
            self.label,
            ',\n'.join([i.repr(indent + '\t') for i in _compartments]),
            ',\n' if len(_compartments) > 0 else '',
            ',\n'.join([i.repr(indent + '\t') for i in _reactions]),
            ',\n' if len(_reactions) > 0 else '',
            ',\n'.join([i.repr(indent + '\t') for i in _species]),
            ',\n' if len(_species) > 0 else '',
            ',\n'.join([i.repr(indent + '\t', k) for k, i in compartments.items()]),
            ',\n' if len(compartments) > 0 else '',
            ',\n'.join([i.repr(indent + '\t', k) for k, i in reactions.items()]),
            ',\n' if len(reactions) > 0 else '',
            ',\n'.join([i.repr(indent + '\t', k) for k, i in species.items()]),
            ',\n' if len(species) > 0 else '',
            #TODO metadata
            ',\n' if len(metadata) > 0 else '',
            indent
        )


if __name__ == '__main__':

    execfile('module1.py')

#    from infobiotics.language import *
#    class C(compartment):
#
#        # attributes
#        a = 10,
#        r = 'a -> b 1'
#
#        # sequences, found by dir...(list)
#        s = ['b -> c 2', species('c', 10), compartment()]
#
#    c = C(
#        species('b', 2), # anonymous species -> could be made an attribute because we know name - but name is not the same as id - need to handle name clashes in sbml, etc
#        'b -> a 0.5', #anonymous reactions
#
#    )
















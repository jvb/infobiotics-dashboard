from infobiotics.commons.quantities.api import metre
import itertools
from species import species
from reactions import reaction 

class compartment(object): pass # forward declaration
    
class basecompartment(object):
    ''' Base class for compartment and metacompartment that implements common functionality. 
    
    Because we want compartment and metacompartment to behaviour similarly it makes sense to put almost everything here.
    
    '''

    reserved_prefixes = ('reserved_prefixes', 'reserved_attribute_name_prefixes', '_', 'species', 'reaction', 'compartment', 'amounts') # catches 'compartments' and 'reactions' properties too because of startswith

    reserved_attribute_name_prefixes = ('_', 'name', 'id', 'volume') # used by metacompartment.__new__ and compartment.__setattr__

    def self_dict_filtered_by_prefix_and_type(self, type):
        return dict((key, value) for key, value in dict((k, getattr(self, k)) for k in [i for i in dir(self) if not i.startswith(reserved_prefixes)]).items() if isinstance(value, type))
    
    def self_dict_filtered_by_prefix_and_type_as_values_list(self, type):
        return self_dict_filtered_by_prefix_and_type(self, type).values()

    @property
    def compartments(self):
#        return self.self_dict_filtered_by_prefix_and_type(self, compartment)
        return self.self_dict_filtered_by_prefix_and_type_as_values_list(self, compartment)

    @property
    def reactions(self):
#        return self.self_dict_filtered_by_prefix_and_type(self, reaction)
        return self.self_dict_filtered_by_prefix_and_type_as_values_list(self, reaction)

    @property
    def species(self):
#        return self.self_dict_filtered_by_prefix_and_type(self, species)
        return self.self_dict_filtered_by_prefix_and_type_as_values_list(self, species)

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

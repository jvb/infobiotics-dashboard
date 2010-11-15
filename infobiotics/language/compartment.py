__all__ = ['compartment']

from core import named
from enthought.traits.api import Either, Instance, List, Tuple, Dict, Str, Int, Float, Any, Property
import itertools
from species import species
from reaction import reaction

CompartmentOrSpeciesOrReactions = Either(

    # compartments
    Instance('compartment'),
    List(Instance('compartment')),
    Tuple(Instance('compartment')),

    # species
#    Int, Quantity, #TODO a=10, a=10*M, a=10*molecules
    Instance('species'),
    List(Instance('species')),
    Tuple(Instance('species')),
    Dict(Str, Int), # initial_amounts = {'a':1} 
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

def filter_by_type(d, type):
    filtered = []

    def fix_missing_id(item, id):
        if hasattr(item, 'id') and item.id == '':
            item.id = id

    def append_item(item, id):
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

class compartment(named):
    volume = Float #TODO make into a litre/length**3 validated Trait
    __ = Any
    _ = CompartmentOrSpeciesOrReactions

    def _trait_added_fired(self, trait):
        ''' Catches attributes added after instantiation. '''
#        print getattr(self, trait)
        print self.trait(trait)

    def __getitem__(self, id):
        for i in itertools.chain(self._species(), self._reactions(), self._compartments()):
#            don't
#            # descend into compartments
#            if isinstance(i, compartment):
#                item = i._get_item(id)
#                if item is not None:
#                    return item
            if i.id == id:
                return i

    def quantity(self, id):
        i = self[id]
        if i is None or not isinstance(i, species):
            raise ValueError('%s is not a species' % id)
        return i.quantity

#    def __class_dir(self):
#        return [name for name in dir(self.__class__) if not name.startswith(('__', '_')) and not callable(getattr(self.__class__, name)) and name != 'wrappers']
#
#    def __class_dir_items(self):
#        return dict([(name, getattr(self.__class__, name)) for name in self.__class_dir()])

    def __dir(self):
        return [name for name in dir(self) if not name.startswith(('__', '_')) and not callable(getattr(self, name)) and name != 'wrappers']

    def __dir_items(self):
        return dict([(name, getattr(self, name)) for name in self.__dir()])

    def __attributes(self, type):
        d = dict(self.__class__.__dict__) # copy items from class dictproxy
        d.update(self.__dict__) # overwrite traits with instances from self
        d.update(self.__dir_items()) # catches attributes of superclasses
        return filter_by_type(d, type)

    def __instance_attributes(self, type):
        d = dict(self.__dict__)
#        d.update(self.__dir_items())
        return filter_by_type(d, type)

    def __class_attributes(self, type):
        d = dict(self.__class__.__dict__)
        d.update(self.__dir_items())#d.update(self.__class_dir_items())
        return filter_by_type(dict(d), type)

    def _species(self):
        #TODO self.__attributes(int)
        # self.__attributes(dict)
        ld = self.__attributes(dict)
        ld = [d for d in ld if isinstance(d.items()[0][0], str) and isinstance(d.items()[0][1], int)]
        print ld

        return self.__attributes(species)

    def _instance_species(self):
        return self.__instance_attributes(species)

    def _class_species(self):
        return self.__class_attributes(species)

    #TODO repeat pattern if it works to make readonly properties
    compartments = Property(trait=List(Instance('compartment')), fget=lambda: self.__attributes(compartment))
#    def _get_compartments(self):
#        return self._compartments()

    def _compartments(self):
        return self.__attributes(compartment)

    def _instance_compartments(self):
        return self.__instance_attributes(compartment)

    def _class_compartments(self):
        return self.__class_attributes(compartment)

    def _reactions(self):
        #TODO self.__attributes(str)
        return self.__attributes(reaction)

    def _instance_reactions(self):
        return self.__instance_attributes(reaction)

    def _class_reactions(self):
        return self.__class_attributes(reaction)


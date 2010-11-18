from basecompartment import basecompartment
from id_generators import template_id_generator
from infobiotics.commons.quantities.api import Quantity
import config
from reactions import reaction
from species import species

class metacompartment(type, basecompartment):

    _id_generator = template_id_generator
    
    def __new__(self, name, bases, dictionary): # see compartment.__init__
        ''' class c(compartment): a = 1, r1='...'
        
        Can directly alter dictionary. 
        
        Should be used for construction.
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        '''
        dictionary['id'] = self._id_generator.next()
        dictionary['name'] = name
        dictionary['bases'] = bases
        
        for key, value in dictionary.items():
            if key.startswith(self.reserved_attribute_name_prefixes):
                continue # deliberately skip the above keys
            if isinstance(value, (int, Quantity)): # convert int/Quantity to species
                s = species(value, name=key)
                dictionary[key] = s
            elif isinstance(value, (str)): # convert str to reaction
                r = reaction(value, name=key, reactants_label=name, products_label=name)
                dictionary[key] = r
            elif config.warn_about_floats and isinstance(value, float):
                sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
            elif isinstance(value, (reaction)):
                print value.metadata #TODO
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

    # because metacompartment doesn't inherit from base (and neither does basecompartment)
    @property
    def metadata(self):
        return dict((k, v) for k, v in self.__dict__.items() if not k.startswith(('_', 'name'))) #TODO add to reserved prefixes?


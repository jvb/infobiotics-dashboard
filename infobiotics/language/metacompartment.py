from compartmentmixin import compartmentmixin
from id_generators import id_generator
from infobiotics.commons.quantities.api import Quantity
import config
from reactions import reaction
from species import species
import sys

class metacompartment(type, compartmentmixin):
    _id_generator = id_generator('t')

    def __new__(self, name, bases, dictionary): # see compartment.__init__
        ''' class c(compartment): a = 1, r1='...'
        
        Can directly alter dictionary. 
        
        Should be used for construction.
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        '''
#        dictionary['_id'] = self._id_generator.next()
        dictionary['label'] = name

        for key, value in dictionary.items():
            if key.startswith(self.reserved_attribute_name_prefixes):
                continue # deliberately skip the above keys
            if isinstance(value, (int, Quantity)): # convert int/Quantity to species
                value = species(name=key, amount=value)
            elif isinstance(value, (basestring)): # convert str to reaction
                try:
                    value = reaction(value, reactants_label=name, products_label=name)
                except ValueError, e:
                    sys.stderr.write(str(e) + ' Setting %s as metadata instead.\n' % name)
            elif isinstance(value, float) and config.warn_about_floats:
                sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
            elif isinstance(value, compartmentmixin):
                value.outside = self
            dictionary[key] = value
        return super(metacompartment, self).__new__(self, name, bases, dictionary)

    def repr(self, indent=''):
        return 'class %s(%s):\n\t%s%s%s' % (
            self.name,
            ', '.join([base.__name__ for base in self.bases]),
            ',\n\t'.join([repr(i) for i in self.species]),
            ',\n\t'.join([repr(i) for i in self.reactions]),
            ',\n\t'.join([repr(i) for i in self.compartments]),
        )

    def str(self, indent=''):
        return 'TODO'


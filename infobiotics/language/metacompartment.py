from compartmentmixin import compartmentmixin
#from id_generators import id_generator
from infobiotics.commons.quantities.api import Quantity
import config
from reactions import reaction
from species import species
import sys
from infobiotics.commons.sequences import flatten

class metacompartment(type, compartmentmixin):

    def __new__(self, name, bases, dictionary): # see compartment.__init__
        ''' class c(compartment): a = 1, r1='...'
        
        Can directly alter dictionary. 
        
        Should be used for construction.
        
        See p59 of Python Metaclasses: Who? Why? When?
        
        
        self == <class '...metacompartment'>
        
        '''
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
                    sys.stderr.write(str(e) + ' Setting %s as metadata instead.\n' % key)
            elif isinstance(value, float) and config.warn_about_floats:
                sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
            elif isinstance(value, compartmentmixin):
                value.outside = self #TODO might be problematic setting outside to metacompartment class
            elif isinstance(value, (list, tuple)):
                for i, item in enumerate(flatten(value)):
                    if isinstance(item, basestring):
                        try:
                            r = reaction(item, reactants_label=name, products_label=name)
                            value[i] = r
                        except ValueError, e:
                            print e
            dictionary[key] = value
        return super(metacompartment, self).__new__(self, name, bases, dictionary)

#    def __init__(self, name, bases, dictionary):
#        ''' self == <class '...compartment'> '''
#        super(metacompartment, self).__init__(name, bases, dictionary)


    # only way to call methods on compartmentmixin is to prefix metaclass and pass class

    def __repr__(self):
        return metacompartment.repr(self)

    def __str__(self):
        return metacompartment.str(self) 

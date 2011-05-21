from compartmentmixin import compartmentmixin
from infobiotics.commons.quantities import *
import config
from reactions import reaction
from species import species
from infobiotics.commons.sequences import iterable, flatten
#import sys
#import logging
#log = logging.getLogger('metacompartment')
#log.addHandler(logging.StreamHandler())
#log.setLevel(logging.WARN)
from infobiotics.commons.api import logging
logger = logging.getLogger(__name__)

class metacompartment(type, compartmentmixin):

    def __new__(metacls, name, bases, dictionary): # see compartment.__init__ @NoSelf
        ''' class c(compartment): a = 1, r1='...'
        
        Features of __new__: (see p59 of Python Metaclasses: Who? Why? When?)
            Can directly alter dictionary. 
            Should be used for construction.
        '''

        if not 'label' in dictionary.keys():
            if name != 'compartment':
                dictionary['label'] = name
            dictionary['_explicitly_labelled'] = False
        else:
            dictionary['_explicitly_labelled'] = True

        dictionary['_bases'] = bases
        for key, value in dictionary.items():
            if key.startswith(metacls.reserved_attribute_name_prefixes):
                continue # deliberately skip the above keys
            if isinstance(value, (int, Quantity)): # convert int/Quantity to species
                try:
                    value = species(name=key, amount=value)
                except ValueError, e:
                    print e
                    value = Quantity(value)
            elif isinstance(value, (basestring)): # convert str to reaction
                try:
                    value = reaction(value, reactants_label=name, products_label=name)
                except ValueError, e:
#                    sys.stderr.write(str(e) + ' Setting %s as metadata instead.\n' % key)
                    log.warn(str(e) + ' Setting %s as metadata instead.' % key)
            elif isinstance(value, float) and config.warn_about_floats:
#                sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
                log.warn("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar)." % name)
            elif isinstance(value, compartment):
                print 'got here'

            elif iterable(value):#elif isinstance(value, (list, tuple)):
                for i, item in enumerate(flatten(value)):
                    if isinstance(item, basestring):
                        try:
                            r = reaction(item, reactants_label=name, products_label=name) #FIXME
                            value[i] = r
                        except ValueError, e:
                            print e
                    elif isinstance(item, species): #TODO
                        raise NotImplementedError
                    elif isinstance(item, compartment): pass #TODO
                        raise NotImplementedError
#            elif
            dictionary[key] = value
        try:
            return super(metacompartment, metacls).__new__(metacls, name, bases, dictionary)
        except TypeError, e:
            reason = '''.
Some of these bases share a common ancestor (making at least one redundant).
Either at least one base should to be removed, or the bases reordered, derived 
classes first, to prevent this error. See: http://bit.ly/ezmEIu'''
            raise TypeError, str(e) + reason


    def __init__(cls, name, bases, dictionary): #@NoSelf
        for key, value in dictionary.items():
            if isinstance(value, compartmentmixin):
                value.outside = cls # update outside #TODO test
            elif key == 'volume' or key == '_volume':
                cls.volume = value
        super(metacompartment, cls).__init__(name, bases, dictionary)

#    def __repr__(cls): # overloading __repr__ enables repr(cls) on compartment classes
#        return cls.repr() # can call normally thanks to mixedmethod # previous had to pass cls to superclass e.g. compartmentmixin.repr(cls) 
#    
#    def __str__(cls): # see __repr__ for hints
#        return cls.str()


if __name__ == '__main__':
    from compartments import compartment
    class c(compartment):
        volume = 10
    print c.volume
    print eval(repr(c.volume))
#    class c(compartment):
#        a = 10
#        d = compartment()
#        m = [compartment(), species('b', 20), 666, 'a 0.1-> b']
#    print c # test overridden __str__
#    print repr(c) # test overridden __repr__ 
#    print c.repr() # test mixedmethod repr

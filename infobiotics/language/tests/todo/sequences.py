''' Sequence attributes.

A sequence is added as a attribute to a compartment class/object, perhaps from
a function that returns rules (a module). What happens? The sequence is 
flattened and iterated over. Any reactions are added to a special (__private or _hidden - test which) variable
because we don't have identifiers with which to add them as attributes to the
class/object. Same for species and compartments. Any unrecognised objects are 
logged. The contents of these variables is used by the relevant property to 
return the 'anonymous' objects as well as getattr'd items from dir(self).
Clashes of 'name' for species should either raise Errors or log warnings.
The mechanism should be factored out into add_species(*species), etc.

One issue might be overwriting of special variables in subclasses (maybe they 
shouldn't be set directly), or maybe not if all addition happens in __init__ 
(compartment) or __new__ (metacompartment). 

'''

from compartments import compartment
from species import species

#import logging
#log = logging.getLogger('language.sequences')
#log.addHandler(logging.StreamHandler())
##log.setLevel(logging.INFO)
##log.setLevel(logging.DEBUG)
#log.setLevel(logging.WARN)
from infobiotics.commons.api import logging
logger = logging.getLogger(__name__)


#def mangled(self, name):
#    if isinstance(self, type):
#        return '_%s__%s' % (self.__name__, name)
#    return '_%s__%s' % (self.__class__.__name__, name)
#
#def get_mangled(self, name):
#    return getattr(self, mangled(self, name))


#def sequences(self, name, value):
#    log.debug("Processing %s as '%s' on %s" % (value, name, self))
#    flattened = flatten(value)
#    rejected = []
#    c = 0
#    for i in flattened:
#        if isinstance(i, compartment):
#            self._compartments.append(i) # don't setattr
##            log.info("Accepted compartment %s from '%s'" % (i, name))
##            log.info("Accepted compartment '%s' from '%s'" % (i.__class__.__name__, name))
#            c += 1
#        else:
#            rejected.append(i)
#    j = 0
#    for i in rejected:
##        log.info("Rejected %s from '%s'" % (i, name))
#        j += 1
#    # don't
##    return
#    if c > 0:
#        log.info("Accepted %s %s from '%s'" % (c, 'compartment' if c == 1 else 'compartments', name))
#    if j > 0:
#        log.info("Rejected %s %s from '%s'" % (j, 'item' if j == 1 else 'items', name))
#    log.debug("Set '%s' on %s to %s" % (name, self, value))


def module(a):
#    print a
    return [compartment(label=a)]


if __name__ == '__main__':

    # class
    class c(compartment):
        a = [compartment(label='c.a')]
        e = module('c.e')
        f = module('c.f')

    # class instance
    ci = c(x=[compartment(label='c().g')])

    # subclass
    class d(c):
        a = [compartment(label='d.a')] # overwrite c.a
        b = [compartment(label='d.b')]
        c = [compartment(label='d.c')]
        e = module('d.e') # overwrite c.e

    # subclass instance
    di = d(
       compartment(name='anon'),
       species('a', 10),
       'xyz: a -> b k=1',
        b=[compartment(label='d().b')], # overwrite d.b 
        d=[compartment(label='d().d')],
#        a=1, c=1, e=1, f=1 # successfully overrides
    )

#    print c.metadata
#    print c().metadata
#    print 'c', c.compartments # c [c.a, c.e, c.f]
#    print 'ci', ci.compartments # ci [c.a, c.e, c.f] # missing c().g
#    print 'd', d.compartments # d [d.a, d.b, d.e, d.c] # missing c.f
#    print di.a, di.c
    print 'di', [c.label for c in di.compartments] # di [d.a, d.b, d.e, d.c] # missing c.f, d().b, d().d 
    print di.species[0].str()
    print di.reactions[0].str()

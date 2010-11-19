from base import base
from basecompartment import basecompartment
from metacompartment import metacompartment
import sys
from id_generators import compartment_id_generator
from infobiotics.commons.quantities.api import Quantity
import config
from species import species
from reactions import reaction


class compartment(base, basecompartment): #@DuplicatedSignature
    __metaclass__ = metacompartment
    _id_generator = compartment_id_generator
#    import module_introspection.ply

    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, (species, compartment, reaction)):
                setattr(self, arg.name, arg)
            elif isinstance(arg, str):
                r = reaction(arg)
                setattr(self, r.name, r)
            else:
#                raise ValueError('%s is not a species, compartment or reaction.' % arg)
                sys.stderr.write("'%s' ignored.\n" % arg)
        base.__init__(self, **kwargs)

    def __setattr__(self, name, value): # see metacompartment.__new__
        ''' compartment().a = 1 and compartment(a=1) '''
        if name.startswith(self.reserved_attribute_name_prefixes):
            super(compartment, self).__setattr__(name, value) # defer to properties
            return
        if isinstance(value, (int, Quantity)):
            value = species(value, name=name)
        elif config.warn_about_floats and isinstance(value, float):
            sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
        elif isinstance(value, (str)):
            value = reaction(value, name=name, reactants_label=self.__class__.__name__, products_label=self.__class__.__name__)
        elif isinstance(value, (reaction)):
            print value.metadata #TODO
#            value = reaction(value, name=name, reactants_label=self.__class__.__name__, products_label=self.__class__.__name__)
        super(compartment, self).__setattr__(name, value)


    def repr(self, indent=''):
        decl = self.__class__.__name__ if self._named else '%s=%s' % (self.id, self.__class__.__name__)
        args = [i for i in self.species if i._named] + [i for i in self.reactions if i._named] + [i for i in self.compartments if i._named]
        kwargs = [i for i in self.species if not i._named] + [i for i in self.reactions if not i._named] + [i for i in self.compartments if not i._named]
        return '%s%s(\n%s%s%s%s%s)' % (
            indent,
            decl,
#            ',\n'.join([i.repr(indent + '\t') for i in self.species]),
#            ',\n' if len(self.species) > 0 else '',
#            ',\n'.join([i.repr(indent + '\t') for i in self.reactions]),
#            ',\n' if len(self.reactions) > 0 else '',
#            ',\n'.join([i.repr(indent + '\t') for i in self.compartments]),
#            ',\n' if len(self.compartments) > 0 else '',
            ',\n'.join([i.repr(indent + '\t') for i in args]),
            ',\n' if len(args) > 0 else '',
            ',\n'.join([i.repr(indent + '\t') for i in kwargs]),
            ',\n' if len(kwargs) > 0 else '',
            indent
        )
        
    def str(self, indent=''):
        return super(base, self).__str__()
        return '%s%s(\n%s%s%s%s%s%s%s)' % (
            indent,
            self.id,
            '\n'.join([i.str(indent + '\t') for i in self.species]),
            '\n' if len(self.species) > 0 else '',
            '\n'.join([i.str(indent + '\t') for i in self.reactions]),
            '\n' if len(self.reactions) > 0 else '',
            '\n'.join([i.str(indent + '\t') for i in self.compartments]),
            '\n' if len(self.compartments) > 0 else '',
            indent
        ) 


if __name__ == '__main__':
    
#    # subclassing correctly *not replaces* but never creates a/s1 in d, only a/s2
#    class c(compartment):
#        a = 1
#    class d(c):
#        a = 2
#    print c.a, c.species, c['s1']
#    print d.a, d.species, d['s1']
    
    
##    # instantiating correctly replaces instance a/s1 with a/s2 without incorrect changing value of class species a/s1  
##    class c(compartment):
##        a = 1
###        a = species(1, 'test', desc='this is a test')
##    print 'c.a', c.a, c.species, c['s1']
##    d = c(a=2)
###    d = c(b=1)
##    print 'c.a', c.a, c.species, c['s1']
##    print 'd.a', d.a, d.species, d['s1']
##    assert c.a.amount == 1
##    print id(c.a)
##    print id(d.a)
##    assert d.a.amount == 2
    
#    # assigning new int to c.a updates existing species
#    c = compartment(a=1)
#    print c.a, c.species
#    c.a = 2
#    print c.a, c.species
#    
#    # assigning new int to c.a updates existing species
#    c = compartment(a=1)
#    print c.a, c.species
#    c.a = '[]_l k-> []_l k=1'
#    print c.a, c.species
    
    
    
#    class c(compartment):
#        a = 4
#    assert c.a.amount == 4 # c is class
#    
#    print c
#    print c.species
#    print c.reactions

    c = compartment(# compartment *args can be species/compartment/reaction() or str but *not* int
        species(6, test=5), #, a), # no name or id should raise ValueError
        species(5, name='b'), #, a), # name but no id should use name as id - if there are no spaces?
        reaction('[ a ]_bacteria k-> [ b ]_bacteria k=0.1'), #, r1),
        reaction('rX: [ b ]_bacteria k-> [ a ]_bacteria k=0.01'), #, r2),
        compartment(
            compartment(a=1),
            a=2,
        ),
        a=3,
        b=1,
        c=0.5,
        d=1,
    )
#    assert c.a.amount == 3 # c is instance
#    print repr(c)
#    print
#    print c.reactions
#    print c.compartments
    print c.species(test=5)
    s = c.species()
    print s
    print s(amount=1)
    print c.species(amount=lambda amount: amount > 1)
    print c.amounts(amount=lambda amount: amount > 1)
    

    r = c.reactions()
    
    # setting a flag on (class) species and using it as metadata
    c.a.flag = True
    print c.amounts(flag=True)

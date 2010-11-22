from base import base
from compartmentmixin import compartmentmixin
from metacompartment import metacompartment
import sys
from id_generators import id_generator
from infobiotics.commons.quantities.api import Quantity
import config
from species import species
from reactions import reaction
from infobiotics.commons.names import find_names

class compartment(compartmentmixin, base):
    __metaclass__ = metacompartment
    _id_generator = id_generator('c')
#    import module_introspection.ply #TODO

    def __init__(self, *args, **kwargs):
        ''' Compartment should have a label which defaults to its class name. '''
        self.label = self.__class__.__name__
        self.outside = None
        for arg in args: # handle anonymous compartments and reactions
            print 'print find_names(arg)', find_names(arg)
            if not isinstance(arg, (compartment, species, reaction, basestring)):
#                sys.stderr.write("'%s' ignored.\n" % arg)
                raise ValueError('Anonymous attributes of a compartment must be either compartments, species or reactions (or strings convertible to reactions).')
            if isinstance(arg, (compartment, reaction, species)):
                if re.match('[_A-Za-z][_A-Za-z1-9]*', arg.name):
                    setattr(self, arg.name, arg) # use name for id if it is a valid Python name
                else:
                    while True: # otherwise generate an id
                        id = arg._id_generator.next()
                        if id not in dir(self): # and if it is not in dir(self) use it
                            setattr(self, id, arg) 
                            break
            elif isinstance(arg, basestring):
                r = reaction(arg)
                setattr(self, r.name, r)
        base.__init__(self, **kwargs) # base will call setattr on all kwargs

    def __setattr__(self, name, value): # see metacompartment.__new__
        ''' compartment().a = 1 and compartment(a=1) '''
        if name.startswith(self.reserved_attribute_name_prefixes):
#            super(compartment, self).__setattr__(name, value) # defer to properties
#            return
            pass # drop to bottom and set
        elif isinstance(value, (int, Quantity)):
            value = species(name=name, value)
        elif isinstance(value, float) and config.warn_about_floats:
            sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
        elif isinstance(value, (basestring)):
            try:
                value = reaction(value, name=name, reactants_label=self.label, products_label=self.label)
            except ValueError, e:
                sys.stderr.write(str(e) + ' Setting %s as metadata instead.\n' % name)
                # value should still be the string so set it as metadata
        elif isinstance(value, compartment):
            value.outside = self
        elif isinstance(value, (list, tuple)):
            from infobiotics.commons.sequence import flatten
            for i in flatten(value):
                setattr(self, name?, value) # there isn't a name! 
                #TODO Add to __species, etc? Name-mangling can be useful to prevent subclasses from overwriting...
                #TODO factor out value changing from __setattr__ so it can be reused for i in flatten(value) #TODO for metacompartment also?
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

# change compartment type in compartmentmixin module
import compartmentmixin
compartmentmixin.compartment = compartment
# necessary to make compartmentmixin().compartments work

if __name__ == '__main__':
    pass
    
    c1 = compartment(desc='desc', ouch='ouch')

    c = compartment(a=c1, d=c1, b=compartment(), f=1, g=2)
#    class c(compartment):
#        a = compartment()
#    print c.species
#    print vars(c)
    print c.compartments
    print 'metadata =', c1.metadata

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
    
    
#    c = compartment(# compartment *args can be species/compartment/reaction() or str but *not* int
#        species(6, test=5), #, a), # no name or id should raise ValueError
#        species(5, name='b'), #, a), # name but no id should use name as id - if there are no spaces?
#        reaction('[ a ]_bacteria k-> [ b ]_bacteria k=0.1'), #, r1),
#        reaction('rX: [ b ]_bacteria k-> [ a ]_bacteria k=0.01'), #, r2),
#        compartment(
#            compartment(a=1),
#            a=2,
#        ),
#        a=3,
#        b=1,
#        c=0.5,
#        d=1,
#    )


#class c(compartment): a = 1; b = 2
#for c in (c, compartment(a=3, b=4, c=5)): 
#
##    print c.repr()
#
##    print c.str()
#
##    print c.compartments
##    print c.compartments()
#
##    print c.reactions
##    print c.reactions()
#
##    print c.species
##    print c.species()
#
#    print c.species(amount=lambda amount: amount > 1) # filter species by amount
##    print c.amounts(amount=lambda amount: amount > 1) # filter amounts by amount
#    
#    # setting a flag on (class) species and using it as metadata
#    c.a.flag = True
##    print c.amounts(flag=True)

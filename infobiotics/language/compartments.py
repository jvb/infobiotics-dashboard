from compartmentmixin import compartmentmixin
from metacompartment import metacompartment
from infobiotics.commons.quantities import *
from species import species
from reactions import reaction
from infobiotics.commons.sequences import iterable, flatten 
import sys
#TODO logging
import config #TODO get log level from config
from infobiotics.language.compartmentmixin import filterablelist

#from infobiotics.commons.metaclasses.noconflict import classmaker
#
#class _compartment(compartmentmixin):
#    __metaclass__ = metacompartment
#
#class compartment(_compartment):
#    __metaclass__ = classmaker(left_metas=(metacompartment,))
#
class compartment(compartmentmixin):
    __metaclass__ = metacompartment

    def add(self, *args):
        for arg in args:
            if isinstance(arg, compartment):
                self._compartments.append(arg)
            elif isinstance(arg, species):
                self._species.append(arg)
            elif isinstance(arg, basestring):
                self._reactions.append(reaction(arg, reactants_label=self.label, products_label=self.label))
            else:
                print "Don't know what to do with %s" % arg

    def __init__(self, *args, **kwargs):
        ''' Compartment should have a label which defaults to its class name. '''

        self.label = self.__class__.__name__
        self.outside = None # overridden in metacompartment.__init__ and compartment.__setattr__
        for k, v in kwargs.items(): setattr(self, k, v)

        # handle anonymous args by putting into private list
        #TODO use list in compartmentmixin.compartments()
        self._compartments = [] #TODO maybe use self._anonymous_compartments instead?
        self._species = []
        self._reactions = []

        for arg in args: # handle anonymous compartments and reactions
            if iterable(arg):#isinstance(arg, (list, tuple)):
                self.add(*flatten(arg))
            else:
                self.add(arg)


    def __setattr__(self, name, value): # see metacompartment.__new__
        ''' compartment().a = 1 and compartment(a=1) '''
        if name.startswith(self.reserved_attribute_name_prefixes):
#            super(compartment, self).__setattr__(name, value) # defer to properties
#            return
            pass # drop to bottom and set
        elif isinstance(value, (int, Quantity)):
            value = species(name=name, amount=value)
        elif isinstance(value, float) and config.warn_about_floats:
            sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
        elif isinstance(value, (basestring)):
            try:
                value = reaction(value, reactants_label=self.label, products_label=self.label)
                #TODO rule_id from name
            except ValueError, e:
                sys.stderr.write(str(e) + ' Setting %s as metadata instead.\n' % name)
                # value should still be the string so set it as metadata
        elif isinstance(value, compartment):
#            if not value == self:
            value.outside = self
#        elif isinstance(value, (list, tuple)): # done in compartmentmixin.compartments()
        super(compartment, self).__setattr__(name, value)


    # overridden properties that append anonymous model items from instances

    @property
    def compartments(self, **metadata): #@UnusedVariable
        ''' Returns a list of all the compartments in the compartment that match the 
        set of *metadata* criteria. '''
        return super(compartment, self).compartments + self._compartments

    @property
    def reactions(self, **metadata): #@UnusedVariable
        ''' Returns a list of all the reactions in the compartment that match the 
        set of *metadata* criteria. '''
        return super(compartment, self).reactions + self._reactions

    @property
    def species(self, **metadata): #@UnusedVariable
        ''' Returns a list of all the species in the compartment that match the 
        set of *metadata* criteria. 
        
        For example, to get all species with amounts > 5:

            >>> from infobiotics.language.compartments import compartment
            >>> c = compartment(a=5,b=6,c=7)
            >>> len(c.species(amount=lambda x: x > 5))
            2

        '''
        return super(compartment, self).species + self._species


# monkey patch compartmentmixin module with compartment type here to avoid circular import earlier
import compartmentmixin
compartmentmixin.compartment = compartment
# necessary to make compartmentmixin().compartments work


if __name__ == '__main__':
    execfile('module1.py')

#    pass
#
#    c1 = compartment(desc='desc', ouch='ouch')
#
#    c = compartment(a=c1, d=c1, b=compartment(), f=1, g=2)
##    class c(compartment):
##        a = compartment()
##    print c.species
##    print vars(c)
#    print c.compartments
#    print 'metadata =', c1.metadata
#
##    # subclassing correctly *not replaces* but never creates a/s1 in d, only a/s2
##    class c(compartment):
##        a = 1
##    class d(c):
##        a = 2
##    print c.a, c.species, c['s1']
##    print d.a, d.species, d['s1']
#
#
###    # instantiating correctly replaces instance a/s1 with a/s2 without incorrect changing value of class species a/s1  
###    class c(compartment):
###        a = 1
####        a = species(1, 'test', desc='this is a test')
###    print 'c.a', c.a, c.species, c['s1']
###    d = c(a=2)
####    d = c(b=1)
###    print 'c.a', c.a, c.species, c['s1']
###    print 'd.a', d.a, d.species, d['s1']
###    assert c.a.amount == 1
###    print id(c.a)
###    print id(d.a)
###    assert d.a.amount == 2
#
##    # assigning new int to c.a updates existing species
##    c = compartment(a=1)
##    print c.a, c.species
##    c.a = 2
##    print c.a, c.species
##    
##    # assigning new int to c.a updates existing species
##    c = compartment(a=1)
##    print c.a, c.species
##    c.a = '[]_l k-> []_l k=1'
##    print c.a, c.species
#
#
##    c = compartment(# compartment *args can be species/compartment/reaction() or str but *not* int
##        species(6, test=5), #, a), # no name or id should raise ValueError
##        species(5, name='b'), #, a), # name but no id should use name as id - if there are no spaces?
##        reaction('[ a ]_bacteria k-> [ b ]_bacteria k=0.1'), #, r1),
##        reaction('rX: [ b ]_bacteria k-> [ a ]_bacteria k=0.01'), #, r2),
##        compartment(
##            compartment(a=1),
##            a=2,
##        ),
##        a=3,
##        b=1,
##        c=0.5,
##        d=1,
##    )
#
#
##class c(compartment): a = 1; b = 2
##for c in (c, compartment(a=3, b=4, c=5)): 
##
###    print c.repr()
##
###    print c.str()
##
###    print c.compartments
###    print c.compartments()
##
###    print c.reactions
###    print c.reactions()
##
###    print c.species
###    print c.species()
##
##    print c.species(amount=lambda amount: amount > 1) # filter species by amount
###    print c.amounts(amount=lambda amount: amount > 1) # filter amounts by amount
##    
##    # setting a flag on (class) species and using it as metadata
##    c.a.flag = True
###    print c.amounts(flag=True)

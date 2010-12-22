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
            elif isinstance(arg, reaction):
                #TODO validate compartment labels
                self._reactions.append(arg)
            elif isinstance(arg, basestring):
                self._reactions.append(reaction(arg))#, reactants_label=self.label, products_label=self.label))
            else:
                print "Don't know what to do with %s" % arg

    def __init__(self, *args, **kwargs):
        '''Each compartment must have a label, which can be defined here or in
        its class definition (defaulting to the class name if not 
        'compartment'), or else a ValueError will be raised.'''

        if not 'label' in kwargs.keys():
            if hasattr(self, 'label'):
                kwargs['label'] = self.label#[:] # copy from class
            else:
                if self.__class__.__name__ != 'compartment':
                    kwargs['label'] = self.__class__.__name__
                else:
                    raise ValueError("""All compartments must have a label, although this can be determined from the class name of a compartment subclass, e.g.
    >>> a = compartment(label='nucleus')
    >>> print a.label
    'nucleus'
    >>> a = vesicle()
    >>> print a.label
    'vesicle'""")
            self._explicitly_labelled = False
        else:
            self._explicitly_labelled = True

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
#        elif isinstance(value, (list, tuple)): # done in compartmentmixin.compartments()
        elif isinstance(value, (int, Quantity)):
            value = species(name=name, amount=value)
        elif isinstance(value, float) and config.warn_about_floats:
            sys.stderr.write("Compartments don't know the meaning of floats like '%s', but they do understand ints (e.g. 10) and quantities (e.g. 0.5 * millimolar).\n" % name)
        elif isinstance(value, (basestring)):
            try:
                value = reaction(value)#TODO, reactants_label=self.label, products_label=self.label)
                setattr(self, name, value) # call this again but with a reaction
                #TODO rule_id from name?
                return #FIXME added early in the morning because what happens when setattr above returns. Do we overwrite it?
            except ValueError, e:
                sys.stderr.write(str(e) + ' Setting %s as metadata instead.\n' % name)
                # value should still be the string so set it as metadata
        elif isinstance(value, reaction):
            # permute reaction?
            value = self.validate_reaction(value)
        elif isinstance(value, compartment):
#            if not value == self:
            value.outside = self
#            if value.label == 'compartment' and name != 'compartment':
#                value.label = name
#            print value.label
        super(compartment, self).__setattr__(name, value)


    def validate_reaction(self, reaction, name=None):
        '''
        
         can:
         '[a]_self ->'
         '[a+b]_self ->'
         '-> a'
         '-> [a]_self'
         '-> [a]_not_self'
         
         can't:
         'a [b]_self ->'
         'a [b]_not_self ->'
         '[a]_not_self ->'
         '-> a [b]_self'
         '-> a [b]_not_self'
         '-> a [b]_self'

        '''
        if len(reaction.reactants_outside) > 0 and len(reaction.reactants_inside) > 0:
            # 'a [b] ->'
            raise ValueError('All reactants have to be in the same source compartment.')
        elif len(reaction.products_outside) > 0 and len(reaction.products_inside) > 0:
            # '-> a [b]'
            raise ValueError('All products have to go to the same target compartment.')
        elif len(reaction.reactants_outside) > 0 and (reaction.reactants_label is None or reaction.reactants_label == self.label):
            # 'a [ ]_y -> [a]_y' can be converted to 'a -> a (y)' in outside compartment
            raise ValueError("Reaction '%s' should go in the enclosing compartment ('%s') as reactions can only push species, not pull them." % (reaction, self.outside.label))
            enclosing = self.outside
            if self.outside is None:
                raise ValueError("No outside compartment to add reaction to.")
            if name is not None:
                setattr(enclosing, name, reaction)
            else:
                enclosing.add(reaction)
            return None
        elif len(reaction.reactants_inside) > 0 and reaction.reactants_label is not None and reaction.reactants_label != self.label:
            raise ValueError("Reaction '%s' should go in the enclosed compartment ('%s') as reactions can only push species, not pull them." % (reaction, reaction.reactants_label))
            enclosed, _ = [compartment for compartment in self.compartments if compartment.label == reaction.reactants_label]
            if name is not None:
                setattr(enclosed, name, reaction)
            else:
                enclosed.add(reaction)
            return None
        elif len(reaction.products_outside) > 0 and reaction.products_label == self.label:
            raise ValueError("Use a transport rule such as 'a -> a (*)' to send species outside the compartment.")
            reaction.vector = '*'
            reaction.is_transport_rule = True
        return reaction


    # overridden properties that append anonymous model items from instances
    # must redeclare property decorator otherwise compartmentmixin methods are 
    # called, see http://books.google.co.uk/books?id=JnR9hQA3SncC&lpg=PA81&ots=JaaTFv-17w&dq=python%20mix%20class%20and%20object%20behaviour&pg=PA101#v=onepage&q&f=false

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
metacompartment.compartment = compartment


if __name__ == '__main__':

#    # labels
#    c = compartment() # raises ValueError
#    c = compartment(label='compartment') # explicitly labelled 'compartment'
#    c = compartment(label='c') # explicitly labelled 'c'
#    class c(compartment): pass # implicitly labelled 'c'
#    print c.str()
#    class c(compartment): label = 'c' # explicitly labelled 'c'
#    print c.str()

#    c = compartment(
#        'a -> [b] 1', # can't know reactants label #TODO make labels mandatory (?)
#        label='c',
#    )
#    print c.str()

    r = reaction('a -> [b] 1')
    print r
    print repr(r.products_outside), repr(r.products_inside)


#    execfile('module1.py')

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
##    print c.amounts(flag=True)

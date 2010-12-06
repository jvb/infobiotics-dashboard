from multiset import multiset
import re
from infobiotics.commons.quantities import *
import config

# use http://re-try.appspot.com/ for live regex matching - use method 'match' and make sure 'VERBOSE' is on

id = r'[_A-Za-z][_A-Za-z1-9]*' # http://homepage.mac.com/s_lott/books/python/html/p04/p04c04_re.html#modules-re

rule_id = r'((?P<rule_id>%s)\s*\:)?' % id # 'r1' from ' r1: '

species = id + r'(\s*\+\s*' + id + r')*' # ab [+ c [+ ...]] but not 2d [+ e]

reactants_outside = r'(?P<reactants_outside>%s)' % species
reactants_inside = r'(?P<reactants_inside>%s)' % species
reactants_label = r'(?P<reactants_label>%s)' % id
reactants = r'(?P<reactants>%s)' % species

products_outside = r'(?P<products_outside>%s)' % species
products_inside = r'(?P<products_inside>%s)' % species
products_label = r'(?P<products_label>%s)' % id
products = r'(?P<products>%s)' % species

number = r'([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'

rate_id = r'(?P<rate_id>(%s|%s))?' % (id, number) # rate_id can nothing, a Python identifer or a number (int or float). Previous -* will greedily match away any '-' (minus) symbols
rate_id2 = r'(?P<rate_id2>(%s|%s))?' % (id, number)

rate = r'(?P<rate>%s)' % number

units = r'(?P<units>[*/]\s*(%s|%s)(\s*[-+*/\^]((?<=\*)[*])?(\s*[()])*\s*(%s|%s)(\s*[()])*)*)?' % (number, id, number, id)
units_unparsed = r'(?P<units_unparsed>([^*/#]??([^#]|[.])*))' # every after parsable units but before comment

#comment = r'(\#\s*(?P<comment>[ ,=+/*\?\-\^()"\'\w\t]+)\s*\#??\s*)?' # everything up to but excluding next '#'
comment = r'(\#\s*(?P<comment>.+))?' # everything else including '#'

## a -> b 0.1e-3 / hour
transformation_rule = r'''
\s*
%s
\s*
(%s?\s*\[\s*%s?\s*\](_%s)?|%s?)
\s*
-*%s-*>
\s*
(%s?\s*\[\s*%s?\s*\](_%s)?|%s?)
(?(products_inside)\s+|\s*)?
(?(products)\s+|\s*)?
(
#?(rate_id)(?P=rate_id)| # relaxed constraint of matching rate_ids 
%s)?
(\s*\=*)?
(\s*%s?\s*%s%s\s*%s)?
''' % (
    rule_id,
    reactants_outside, reactants_inside, reactants_label, reactants,
    rate_id,
    products_outside, products_inside, products_label, products,
    rate_id2,
    rate, units, units_unparsed, comment,
)
##print transformation_rule
#print "transformation_rule = r'''%s'''" % transformation_rule
#transformation_rule = r'''
#\s*
#((?P<rule_id>[_A-Za-z][_A-Za-z1-9]*)\s*\:)?
#\s*
#((?P<reactants_outside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\[\s*(?P<reactants_inside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\](_(?P<reactants_label>[_A-Za-z][_A-Za-z1-9]*))?|(?P<reactants>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?)
#\s*
#-*(?P<rate_id>([_A-Za-z][_A-Za-z1-9]*|([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?))?-*>
#\s*
#((?P<products_outside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\[\s*(?P<products_inside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\](_(?P<products_label>[_A-Za-z][_A-Za-z1-9]*))?|(?P<products>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?)
#(?(products_inside)\s+|\s*)?
#(?(products)\s+|\s*)?
#(
##?(rate_id)(?P=rate_id)| # relaxed constraint of matching rate_ids 
#(?P<rate_id2>([_A-Za-z][_A-Za-z1-9]*|([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?))?)?
#(\s*\=*)?
#(\s*(?P<rate>([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)?\s*(?P<units>[*/]\s*(([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?|[_A-Za-z][_A-Za-z1-9]*)(\s*[-+*/\^]((?<=\*)[*])?(\s*[()])*\s*(([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?|[_A-Za-z][_A-Za-z1-9]*)(\s*[()])*)*)?(?P<units_failed>([^*/#]??([^#]|[.])*))\s*(\#\s*(?P<comment>.+))?)?
#'''
#exit()
transformation_rule_matcher = re.compile(transformation_rule, re.VERBOSE)

vector = r'\(\s*(?P<vector>[-+]?\d+\s*,\s*[-+]?\d+\s*)\)'
#vector2 = r'\(\s*(?P<vector2>[-+]?\d+\s*,\s*[-+]?\d+\s*)\)'

# a -> b (0,1) 0.1e-3 / hour
transport_rule = r'''
\s*
%s
\s*
(%s?\s*\[\s*%s?\s*\](_%s)?|%s?)
\s*
-*%s-*>
\s*
(%s?\s*\[\s*%s?\s*\](_%s)?|%s?)
(?(products_inside)\s+|\s*)?
(?(products)\s+|\s*)?
%s\s*
(
#?(rate_id)(?P=rate_id)| # relaxed constraint of matching rate_ids 
%s)?
(\s*\=*)?
(\s*%s?\s*%s%s\s*%s)?
''' % (
    rule_id,
    reactants_outside, reactants_inside, reactants_label, reactants,
    rate_id, # doubles as rate
    products_outside, products_inside, products_label, products,
    vector,
    rate_id2, # doubles as rate_id and therefore rate
    rate, units, units_unparsed, comment,
)
##print transport_rule
#print "transport_rule = r'''%s'''" % transport_rule
#transport_rule = r'''
#\s*
#((?P<rule_id>[_A-Za-z][_A-Za-z1-9]*)\s*\:)?
#\s*
#((?P<reactants_outside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\[\s*(?P<reactants_inside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\](_(?P<reactants_label>[_A-Za-z][_A-Za-z1-9]*))?|(?P<reactants>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?)
#\s*
#-*(?P<rate_id>([_A-Za-z][_A-Za-z1-9]*|([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?))?-*>
#\s*
#((?P<products_outside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\[\s*(?P<products_inside>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?\s*\](_(?P<products_label>[_A-Za-z][_A-Za-z1-9]*))?|(?P<products>[_A-Za-z][_A-Za-z1-9]*(\s*\+\s*[_A-Za-z][_A-Za-z1-9]*)*)?)
#(?(products_inside)\s+|\s*)?
#(?(products)\s+|\s*)?
#\(\s*(?P<vector>[-+]?\d+\s*,\s*[-+]?\d+\s*)\)\s*
#(
##?(rate_id)(?P=rate_id)| # relaxed constraint of matching rate_ids 
#(?P<rate_id2>([_A-Za-z][_A-Za-z1-9]*|([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?))?)?
#(\s*\=*)?
#(\s*(?P<rate>([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)?\s*(?P<units>[*/]\s*(([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?|[_A-Za-z][_A-Za-z1-9]*)(\s*[-+*/\^]((?<=\*)[*])?(\s*[()])*\s*(([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?|[_A-Za-z][_A-Za-z1-9]*)(\s*[()])*)*)?(?P<units_unparsed>([^*/#]??([^#]|[.])*))\s*(\#\s*(?P<comment>.+))?)?
#'''
#exit()
transport_rule_matcher = re.compile(transport_rule, re.VERBOSE)

# [ PQS ]_medium == ( 1, 0 ) == [   ] -1.0-> [   ]_medium = (  1, 0 ) = [PQS] d = 100   # comment #
#   ___             ________           _____                                  _______
# PQS -> (1, 0) 0.1
# PQS -> (1, 0) x=0.1
# PQS 0.1-> (1, 0)
# PQS x-> (1, 0) x=0.1
# reaction('PQS -> (1,0)', rate=0.1)
# reaction('PQS x-> (1,0)', x=0.1)
# reaction('PQS -> (1,0)' x, x=0.1)
# reaction('PQS -> (1,0) x', x=0.1, rate=0.2)
# a -> b (1,0) 0.1
# r1 : [PQS]_medium===(1,0)=[  ]-1.0->[  ]_medium(1,0)[PQS]d=100#visible #hidden
# a -> [b]_error  


class reaction(object):

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()

    def repr(self, indent='\t', indent_level=0, id=''):
#        return "%s%s%sreaction(reactants_outside=%r, reactants_inside=%r, reactants_label='%s', products_outside=%r, products_inside=%r, products_label='%s', rate=%s)" % (indent, id, '=' if id != '' else '', self.reactants_outside, self.reactants_inside, self.reactants_label, self.products_outside, self.products_inside, self.products_label, self.rate)
        return "%s%s%sreaction('%s')" % (indent * indent_level, id, '=' if id != '' else '', self.str())

    def str(self, indent='', indent_level=0, comment=False):
        reactants = multiset(self.reactants_outside + self.reactants_inside)
        products = multiset(self.products_outside + self.products_inside)
        if len(self.reactants_inside) == len(reactants) and len(self.products_inside) == len(products):
            return '%s -> %s %s' % (self.reactants_inside, self.products_inside, self.rate) 
        return self.iml(indent, indent_level, comment)
    
    def iml(self, indent='', indent_level=0, comment=False, volume=1 * metre ** 3):
        return '%s%s%s[ %s ]%s -%s-> %s%s[ %s ]%s %s=%s %s' % (
            indent * indent_level,
            self.reactants_outside if self.reactants_outside is not None else '',
            ' ' if len(self.reactants_outside) > 0 else '',
            self.reactants_inside if self.reactants_inside is not None else '',
            '_' + self.reactants_label if self.reactants_label is not None else '_l',
            self.rate_id if self.rate_id is not None else 'c',
            self.products_outside if self.products_outside is not None else '',
            ' ' if len(self.products_outside) > 0 else '',
            self.products_inside if self.products_inside is not None else '',
            '_' + self.products_label if self.products_label is not None else '_l',
            self.rate_id if self.rate_id is not None else 'c',
            str(self.rate) if volume is None else str(stochastic_rate_constant(self, volume=volume)),
            '' if not comment or self.comment is None else '# %s #' % self.comment#.replace('','') #TODO get rid of bad characters for IML
        )

    def __init__(self, rule=None, rate=None, **kwargs):
        '''Uni- or bimolecular reaction that either transforms or transports
        molecular species in a compartment and possibly between an enclosed, 
        enclosing or neighbouring compartment.  
        
        Keyword arguments (*kwargs*) and *rate* will override values from 
        *rule*.
        
        '''

        # set defaults
        self.rule_id = None
        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = None
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = None
        self.rate_id = None
        self.rate_id2 = None
        self.rate = rate # won't be overwritten by rule
        self.comment = None

#        self.reactant_label = None
#        self.reactant_here = multiset()
#        self.vector = None
#        self.reactant_label2 = None
#        self.vector2 = None
#        self.product_there = multiset()

        # set kwargs that rate_id might refer to
        for k, v in kwargs.items(): setattr(self, k, v)

        if rule is not None:
            if not isinstance(rule, basestring):
                raise ValueError("Reaction rule '%s' is not a string." % rule)
            self.extract_from_rule(rule)

        # override rule values with kwargs #TODO ?
        for k, v in kwargs.items(): setattr(self, k, v)

        if self.rate is None:
            raise ValueError("No rate could be determined for reaction%s." % " '%s'" % rule if rule is not None else '')

        # validation

#        if len(self.reactants_outside) > 2:
#            raise ValueError("Rule ' % s' has too many reactants outside, a maximum of 2 reactants is permitted for any reaction." % self.str())
#        elif len(self.reactants_inside) > 2:
#            raise ValueError("Rule ' % s' has too many reactants inside %s, a maximum of 2 reactants is permitted for any reaction." % (self.str(), self.reactants_label))
#        elif len(self.reactants_outside) + len(self.reactants_inside) > 2:
#            raise ValueError("Rule ' % s' has too many reactants, a maximum of 2 reactants is permitted for any reaction." % self.str())
        less_than_1_reactant_error = ValueError("mcss cannot handle reactions with less than 1 reactant '%s'." % reaction)
        more_than_2_reactants_error = ValueError("mcss cannot handle reactions with more than 2 reactants '%s'." % reaction)
        if self.has_zeroth_order_reactants():
            raise less_than_1_reactant_error
        elif not any((self.has_first_order_reactants(), self.has_second_order_homo_reactants(), self.has_second_order_hetero_reactants())):
            raise more_than_2_reactants_error


        if self.rate is None and self.rate_id is None:
            print 'got here'

#        if self.rate_id is None and self.rate_id2 is None:
#            print 'a -> b

#        # rate is stochastic rate constant already (?)
#        if reaction.has_first_order_rate():
#            if not reaction.has_first_order_reactants():
#                if reaction.has_second_order_homo_reactants():
#                    config.log.info("Using first order rate for homogenous second order reaction '%s'." % reaction)
#                elif reaction.has_second_order_hetero_reactants():
#                    config.log.info("Using first order rate for heterogenous second order reaction '%s'." % reaction)
##                if reaction.has_zeroth_order_reactants():
##                    config.log.info("Using first order rate for zeroth order reaction '%s'." % reaction)
##                else:
##                    raise more_than_2_reactants_error

        # test whether rate with units can be converted into a stochastic rate constant 
        if self.has_zeroth_order_rate():
            try:
                self.rate.rescale(molar / second)
            except ValueError:
                raise ValueError("Cannot convert deterministic reaction rate constant '%s' for reaction '%s'." % (self.rate, reaction))
        elif self.has_first_order_rate():
            pass # no conversion necessary
        elif self.has_second_order_rate():
            try:
                V = 1 * metre ** 3
                N = N_A * (mole ** -1)
                self.rate.rescale(molar ** -1 * second ** -1) / (N * V)
            except ValueError:
                raise ValueError("Cannot convert deterministic reaction rate constant '%s' for reaction '%s'." % (self.rate, reaction))
        elif self.has_equilibrium_dissociation_rate():
            try:
                self.rate * config.k_on_max
            except ValueError:
                raise ValueError("Cannot convert equilibrium constant '%s' for reaction '%s'." % (self.rate, reaction))
        else:
            print 'got here'


    @classmethod
    def create_from_rule(cls, rule, rate=None, **kwargs):
        
        is_transport_rule = False
        if transformation_rule_matcher.match(rule):
            match = transformation_rule_matcher.match(rule)
        elif transport_rule_matcher.match(rule):
            match = transport_rule_matcher.match(rule)
            is_transport_rule = True
        else:
            raise ValueError("Failed to create reaction from rule '%s'.\nAll rules require at least one space before '->'." % rule) #TODO examples of valid rules
        kwargs['is_transport_rule'] = is_transport_rule
        
        if rate is not None:
            kwargs['rate'] = rate
        else:
            kwargs['rate'] = None

        reactants_set = False
        products_set = False
        for name, value in match.groupdict().items():
            if name in ('reactants_outside', 'reactants_inside',
                        'products_outside', 'products_inside',
                        'reactants', 'products',
            ):
                # reactants or products are specified only when '[ ]' missing
                if name == 'reactants' and value is not None:
                    reactants_set = True
                elif name == 'products' and value is not None:
                    products_set = True
                if name == 'reactants_inside' and reactants_set:
                    continue
                elif name == 'products_inside' and products_set:
                    continue
                if name == 'reactants':
                    name = 'reactants_inside'
                elif name == 'products':
                    name = 'products_inside'
                if value is not None:
                    # can construct multiset from a list of str where the same str value might appear more than once
                    value = multiset([s.strip() for s in value.split(' + ')])
                    del s # remove variable 's' from locals() as it could interfere with rate units
                else:
                    value = multiset()
            elif name == 'rate_id':
                if value is None:
                    continue # don't overwrite value from rate_id if already set
            elif name == 'rate_id2':
                if match.groupdict()['rate_id'] is None:
#                    if value is None:
#                        raise ValueError('rate_id2 ignored if rate_id set otherwise mandatory')
                    name = 'rate_id'
            elif name in ('reactants_label', 'products_label') and value is None: #TODO do same for 'label' as for reactants and products
                continue
            elif name == 'rate':
                if 'rate' in kwargs.keys() and kwargs['rate'] is not None:
                    continue # don't overwrite rate
            elif name == 'comment' and value is not None:
                value = value.strip()
            kwargs[name] = value


        if kwargs['rate'] is None and kwargs['rate_id'] is None:
            print 'got here'

#        if kwargs['rate_id'] is None and kwargs['rate_id2'] is None:
#            print 'a -> b'

        # if kwargs['rate'] is None
        # try and get rate from (in this order):
        #     rate group in rule, 
        #     rate metadata on reaction, # enables generic overriding
        #     metadata attribute with same name as rule_id on reaction
        # see test_reaction_rate.py  

        if kwargs['rate'] is None and kwargs['rate_id'] is not None:
            kwargs['rate'] = kwargs['rate_id']

        if isinstance(kwargs['rate'], basestring):
            try:
                kwargs['rate'] = float(kwargs['rate'])
            except ValueError:
                try:
                    kwargs['rate'] = float(getattr(self, kwargs['rate_id']))
                    kwargs['rate_id'] = 'c' # since rate_id is number we should make it a generic label
                except ValueError, e: # float conversion failed
                    raise ValueError("Couldn't assign a rate for rule '%s' from 'rate'." % rule)
                except AttributeError, e: # no attribute with name rate_id
                    raise AttributeError("Couldn't assign a rate for rule '%s' from 'rate' or '%s'." % (rule, kwargs['rate_id']))

        if not isinstance(kwargs['rate'], Quantity):
            
            if len(kwargs['units_unparsed']) > 0:
                if kwargs['units'] is not None:
                    raise ValueError("Couldn't parse rate units completely, parsed '%s' but not '%s'." % (kwargs['units'], kwargs['units_unparsed']))
                raise ValueError("Couldn't parse rate units '%s'." % kwargs['units_unparsed'])
            # else rate and/or units was immediately followed by a comment or nothing
            
            if isinstance(kwargs['rate'], (int, float)):
                if kwargs['units'] is None: # rate was immediately followed by a comment or nothing
                    # assume rate is stochastic rate per default time units #TODO log?
                    kwargs['rate'] = kwargs['rate'] / config.time_units  # creates Quantity
                else:
                    kwargs['units'] = kwargs['units'].replace('^', '**')
                    try:
                        kwargs['rate'] = eval(kwargs['rate'] + kwargs['units']) # creates Quantity
                        # rate and units are syntactically OK
                    except SyntaxError, e:
                        print e
                        kwargs['units'] = kwargs['units'].strip()
                        error = "Couldn't find or parse rate units ' % s'." % kwargs['units']
                        ch = kwargs['units'][0]
                        if ch not in ' */ ':
                            error += " Rate must be either multiplied ('*') or divided (' / ') by units, e.g. '0.1e-2 * (micromolar / second)'."
                        print error
            else:
                # not a Quantity, str, int or float
                raise ValueError('Unknown rate type.')

        #TODO check units are semantically OK

        return reaction(**kwargs)


    def extract_from_rule(self, rule):
        is_transport_rule = False
        if transformation_rule_matcher.match(rule):
            match = transformation_rule_matcher.match(rule)
        elif transport_rule_matcher.match(rule):
            match = transport_rule_matcher.match(rule)
            is_transport_rule = True
        else:
            raise ValueError("Failed to create reaction from rule '%s'.\nAll rules require at least one space before '->'." % rule) #TODO examples of valid rules
        self.is_transport_rule = is_transport_rule
        
        reactants_set = False
        products_set = False
        for name, value in match.groupdict().items():
            if name in ('reactants_outside', 'reactants_inside',
                        'products_outside', 'products_inside',
                        'reactants', 'products',
            ):
                # reactants or products are specified only when '[ ]' missing
                if name == 'reactants' and value is not None:
                    reactants_set = True
                elif name == 'products' and value is not None:
                    products_set = True
                if name == 'reactants_inside' and reactants_set:
                    continue
                elif name == 'products_inside' and products_set:
                    continue
                if name == 'reactants':
                    name = 'reactants_inside'
                elif name == 'products':
                    name = 'products_inside'
                if value is not None:
                    # can construct multiset from a list of str where the same str value might appear more than once
                    value = multiset([s.strip() for s in value.split(' + ')])
                    del s
                else:
                    value = multiset()
            elif name == 'rate_id':
                if value is None:
                    continue # don't overwrite value from rate_id if already set
            elif name == 'rate_id2':
                if match.groupdict()['rate_id'] is None:
#                    if value is None:
#                        raise ValueError('rate_id2 ignored if rate_id set otherwise mandatory')
                    name = 'rate_id'
            elif name in ('reactants_label', 'products_label') and value is None: #TODO do same for 'label' as for reactants and products
                continue
            elif name == 'rate':
                if hasattr(self, 'rate') and self.rate is not None:
                    continue
            elif name == 'comment' and value is not None:
                value = value.strip()
            setattr(self, name, value)

        if self.rate is None and self.rate_id is None:
            print 'got here'

#        if self.rate_id is None and self.rate_id2 is None:
#            print 'got here too'

        # if self.rate is None
        # try and get rate from (in this order):
        #     rate group in rule, 
        #     rate metadata on reaction, # enables generic overriding
        #     metadata attribute with same name as rule_id on reaction
        # see test_reaction_rate.py  

        if self.rate is None and self.rate_id is not None:
            self.rate = self.rate_id

        if isinstance(self.rate, basestring):
            try:
                self.rate = float(self.rate)
            except ValueError:
                try:
                    self.rate = float(getattr(self, self.rate_id))
                    self.rate_id = 'c' # since rate_id is number we should make it a generic label
                except ValueError, e: # float conversion failed
                    raise ValueError("Couldn't assign a rate with id '%s' from metadata: %s" % (self.rate_id, e))
                except AttributeError, e: # no attribute with name rate_id
                    raise AttributeError("Couldn't assign a rate with id '%s' from metadata: %s" % (self.rate_id, e))

        if not isinstance(self.rate, Quantity):

            if len(self.units_unparsed) > 0:
                if self.units is not None:
                    raise ValueError("Couldn't parse rate units completely, parsed '%s' but not '%s'." % (self.units, self.units_unparsed))
                raise ValueError("Couldn't parse rate units '%s'." % self.units_unparsed)
            # else rate and/or units was immediately followed by a comment or nothing

            if isinstance(self.rate, (int, float)):
                if self.units is None:
                    if self.units_unparsed is None: 
                        # assume rate is stochastic rate per default time units #TODO log?
                        self.rate = self.rate / config.time_units  # creates Quantity
                else:
                    self.units = self.units.replace('^', '**')
                    try:
                        self.rate = eval('%s%s' % (self.rate, self.units)) # creates Quantity
                        # rate and units are syntactically OK
                    except SyntaxError, e:
                        print e
                        self.units = self.units.strip()
                        error = "Couldn't find or parse rate units '%s'." % self.units
                        ch = self.units[0]
                        if ch not in '*/':
                            error += " Rate must be either multiplied ('*') or divided ('/') by units, e.g. '0.1e-2 * (micromolar / second)'."
                        print error
            else:
                # not a Quantity, str, int or float
                raise ValueError('Unknown rate type.')
        else:
            # set self.units from Quantity
            self.units = self.rate.dimensionality #TODO test

        #TODO check units are semantically OK


    def has_zeroth_order_reactants(self):
        reactants = multiset(self.reactants_outside + self.reactants_inside)
        return True if len(reactants) == 0 else False

    def has_first_order_reactants(self):
        reactants = multiset(self.reactants_outside + self.reactants_inside)
        return True if len(reactants) == 1 and reactants.cardinality() == 1 else False

    def has_second_order_homo_reactants(self):
        '''a+a[], a+a=[a+a] hom'''
        return True if (len(self.reactants_outside) == 1 and self.reactants_outside.cardinality() == 2) or (len(self.reactants_inside) == 1 and self.reactants_inside.cardinality() == 2) else False

    def has_second_order_hetero_reactants(self):
        '''a[a], a[b], a+b[], a+b=[a+b] het'''
        reactants = multiset(self.reactants_outside + self.reactants_inside)
        if reactants.cardinality() != 2:
            return False
        if len(reactants) == 1: # a[a]
            if self.reactants_outside.cardinality() != 1 or self.reactants_inside.cardinality() != 1:
                return False
            return True
        elif len(reactants) == 2:
            if (self.reactants_outside.cardinality() == 1 and self.reactants_inside.cardinality() == 1) or (self.reactants_outside.cardinality() == 2 and self.reactants_inside.cardinality() == 0) or (self.reactants_outside.cardinality() == 0 and self.reactants_inside.cardinality() == 2):
                return True
        return False


    def can_rescale_rate(self, unitquantity):
        try:
            self.rate.rescale(unitquantity)
        except ValueError, e: # couldn't rescale
#            print e
            return False
        except AttributeError, e: # rate is float or int
#            print e
            return False
        return True

    def has_zeroth_order_rate(self):
        return self.can_rescale_rate(molar * config.time_units ** -1)

    def has_first_order_rate(self):
        return self.can_rescale_rate(config.time_units ** -1)

    def has_second_order_rate(self):
        return self.can_rescale_rate((molar ** -1) * (config.time_units ** -1))

    def has_equilibrium_dissociation_rate(self):
        return self.can_rescale_rate(molar)


def stochastic_rate_constant(reaction, volume=1):
    '''Checks whether rate constant is appropriate for reactants and raises ValueError if conversion not possible.'''

    V = volume.rescale(metre ** 3)
    N = N_A * (mole ** -1)

    k = reaction.rate

    if k < 0:
        raise ValueError('Reaction rates cannot be less than zero.')

    k_on_max = config.k_on_max
    if reaction.has_equilibrium_dissociation_rate():
        K_D = k
#        del(k)

    # convert rate to first order if not a quantity     
    if isinstance(reaction.rate, (int, float)):
        k = k * config.time_units ** -1

    #TODO zeroth order too and reactants in different compartments (and products!)
    more_than_3_reactants_error = ValueError("Stochastic simulation algorithm cannot handle reactions with more than 2 reactants '%s'." % reaction)

    # rate is stochastic rate constant already (?)
    if reaction.has_first_order_rate():
        if not reaction.has_first_order_reactants():
            if reaction.has_zeroth_order_reactants():
                config.log.info("Using first order rate for zeroth order reaction '%s'." % reaction)
            elif reaction.has_second_order_homo_reactants():
                config.log.info("Using first order rate for homogenous second order reaction '%s'." % reaction)
            elif reaction.has_second_order_hetero_reactants():
                config.log.info("Using first order rate for heterogenous second order reaction '%s'." % reaction)
            else:
                raise more_than_3_reactants_error
        c = k.rescale(config.time_units ** -1)

    if reaction.has_zeroth_order_reactants():
        if reaction.has_zeroth_order_rate():
            # convert to first order
            c = (N * V * k.rescale(molar / second)).rescale(config.time_units ** -1)
        else:
            raise ValueError("Cannot convert deterministic reaction rate constant '%s' for zeroth order reaction '%s'." % (k, reaction))
    elif reaction.has_first_order_reactants():
        if reaction.has_first_order_rate():
            # rescale rate to config.time_units
            c = k.rescale(config.time_units ** -1) # don't expect to ever reach here
        elif reaction.has_equilibrium_dissociation_rate():
            # use K_D and k_on_max to calculate k_off 
            k_off = K_D * k_on_max
            c = k_off.rescale(config.time_units ** -1)
        else:
            raise ValueError("Cannot convert deterministic reaction rate constant '%s' for first order reaction '%s'." % (k, reaction))
    elif reaction.has_second_order_homo_reactants():
        if reaction.has_second_order_rate():
            # convert rate to first order 
            c = ((2 * k.rescale(molar ** -1 * second ** -1)) / (N * V)).rescale(config.time_units ** -1)
        elif reaction.has_equilibrium_dissociation_rate():
            # use k_on_max instead #TODO log this
            c = ((2 * k_on_max.rescale(molar ** -1 * second ** -1)) / (N * V)).rescale(config.time_units ** -1)
        else:
            raise ValueError("Cannot convert deterministic reaction rate constant '%s' for homogenous second order reaction '%s'." % (k, reaction))
    elif reaction.has_second_order_hetero_reactants():
        if reaction.has_second_order_rate():
            # convert rate to first order
            c = (k.rescale(molar ** -1 * second ** -1) / (N * V)).rescale(config.time_units ** -1)
        elif reaction.has_equilibrium_dissociation_rate():
            # use k_on_max instead
            c = (k_on_max.rescale(molar ** -1 * second ** -1) / (N * V)).rescale(config.time_units ** -1)
        else:
            raise ValueError("Cannot convert deterministic reaction rate constant '%s' for heterogenous second order  '%s'." % (k, reaction))
    else:
        raise more_than_3_reactants_error
#    print c
    return c


    #TODO transport reaction rates
    '''
    c = D/L**2
    
    D = m ** 2 / second # Diffusion coefficient for a particular molecule
    
    L = centroid to centroid length in m (changes with volume - assume cube of side length L)
    
    :*
    
    if scale_transport_rules=true then c == D else c == c
        
    '''




if __name__ == '__main__':


    from infobiotics.language import *

    r = reaction('a + a -> b 0.1e-3 * M / s')
    print r, r.iml()
    print reaction.create_from_rule('a -> b', 7 * molar).iml()

#    r = reaction('a -> b 0.1e-3  molar^-1 * s**-1')

#    r1 = reaction('a -> b 5*10^-3 M^-1 s**-1')
#    print r1
#
#    r2 = reaction('a -> b', rate=5e-3 * M ** -1 * seconds ** -1)
#    print r2

#    units = M ** -1 * seconds ** -1
#
#    rates = np.linspace(0, 1, 11)
#
#    for rate in rates:
#        print rate * units,
#        system = model(compartment(reaction('a -> b', rate=rate)))
#    print
#    print system



    from infobiotics.commons.ordereddict import OrderedDict
    parameters = OrderedDict([
        ('g_S0', 0.1 * micromolar / hour),
        ('g_SA', 1.0 * micromolar / hour),
        ('h_A', 2),
        ('K_SA', 0.2 * micromolar),
        ('k_+S', 100 / hour),
        ('h_Q', 2),
        ('K_S', 0.008 * micromolar),
        ('k_+p', 250 / micromolar / hour), # changed 'K' to 'k' in 'k_+p'
        ('k_-p', 200 / micromolar / hour),
        ('k_D', 90 / hour),
        ('m_s', 1.5 / hour),
        ('g_A', 10 / hour),
        ('m_A', 1 / hour),
        ('K_XI', .005 * micromolar),
        ('K_ZI', .005 * micromolar),
        ('h_I', 2),
        ('g_X0', 0 * micromolar / hour),
        ('g_Z0', 0 * micromolar / hour),
        ('K_XA', 0.1 * micromolar),
        ('K_ZA', 0.2 * micromolar),
        ('h_A', 2),
        ('g_XA', 3.33 * micromolar / hour),
        ('g_ZA', 1.67 * micromolar / hour),
        ('k_+RX', 14 / micromolar / hour),
        ('k_-RX', 1 / hour),
        ('k_+EX', 17 / micromolar / hour),
        ('k_-EX', 1 / hour),
        ('k_+RZ', 14 / micromolar / hour),
        ('k_-RZ', 1 / hour),
        ('k_+EZ', 20 / micromolar / hour),
        ('k_-EZ', 1 / hour),
        ('n', 4),
        ('m_X', 15 / hour),
        ('m_Z', 7 / hour),
        ('g_R', 0.3 * micromolar / hour),
        ('m_R', 1 / hour),
        ('g_E', 12 * micromolar / hour),
        ('K_ER', 0.2 * micromolar),
        ('K_EE', 0.2 * micromolar),
        ('m_E', 1 / hour),
        ('m_RX', 1.5 / hour),
        ('m_EX', 1.5 / hour),
        ('m_RZ', 1.5 / hour),
        ('m_EZ', 1.5 / hour),
        ('g_I', 0.5 * micromolar / hour),
        ('K_IR', 0.005 * micromolar),
        ('K_IE', 0.038 * micromolar),
        ('m_I', 3 / hour),
        ('g_Q', 120 * uM / h),
        ('K_QR', 0.04 * micromolar),
        ('K_QE', 0.1 * micromolar),
        ('m_Q', 10 / hour),
        ('m_QE', 10 / hour),
        ('d', 100 / hour),
        ('w', 0.02), #* litre),
        ('m_B', 0.05 / hour),
    ])

    zeroth = reaction(' ->a', 1)
    first = reaction('a ->  ', 1)
    second_homo = reaction('a + a ->  ', 1)
    second_hetero = reaction('a + b ->  ', 1)

#    import config
#    config.time_units = hour
#    for parameter, rate in parameters.items():
#        print parameter
#        for r in (zeroth, first, second_homo, second_hetero):
#            r.rate_id = parameter
#            r.rate = rate
#            print r.has_zeroth_order_rate(), r.has_first_order_rate(), r.has_second_order_rate(), r.has_equilibrium_dissociation_rate(),
#            try:
#                c = stochastic_rate_constant(r, 1 * (micro * metre) ** 3)
#                print r, rate, c
#            except ValueError, e:
#                print e
#                pass
#        print
#    exit()


    # test reaction.has_*_order_reactants(self) #TODO move to test suite

    assert     zeroth.has_zeroth_order_reactants() # '->a' fails. #TODO allow zeroth order reactions?
    assert not zeroth.has_first_order_reactants()
    assert not zeroth.has_second_order_homo_reactants()
    assert not zeroth.has_second_order_hetero_reactants()

    assert not first.has_zeroth_order_reactants()
    assert     first.has_first_order_reactants()
    assert not first.has_second_order_homo_reactants()
    assert not first.has_second_order_hetero_reactants()

    assert not second_homo.has_zeroth_order_reactants()
    assert not second_homo.has_first_order_reactants()
    assert     second_homo.has_second_order_homo_reactants()
    assert not second_homo.has_second_order_hetero_reactants()
    assert not reaction('a [a] ->  ', 1).has_second_order_homo_reactants()

    assert not second_hetero.has_zeroth_order_reactants()
    assert not second_hetero.has_first_order_reactants()
    assert not second_hetero.has_second_order_homo_reactants()
    assert     second_hetero.has_second_order_hetero_reactants()
    assert     reaction('a [a] ->  ', 1).has_second_order_hetero_reactants()

    assert not reaction('a + a + a ->  ', 1).has_zeroth_order_reactants()
    assert not reaction('a + a + a ->  ', 1).has_first_order_reactants()
    assert not reaction('a + a + a ->  ', 1).has_second_order_homo_reactants()
    assert not reaction('a + a + a ->  ', 1).has_second_order_hetero_reactants()


    # test reaction.has_*_order_rate(self) #TODO move to test suite

    rate = 1.0
    zeroth = rate * millimolar * config.time_units ** -1
    first = rate * config.time_units ** -1
    second = rate * ((molar ** -1) * (config.time_units ** -1))
    K_D = rate * molar

    assert     reaction(rate=zeroth).has_zeroth_order_rate()
    assert not reaction(rate=first).has_zeroth_order_rate()
    assert not reaction(rate=second).has_zeroth_order_rate()
    assert not reaction(rate=K_D).has_zeroth_order_rate()

    assert not reaction(rate=zeroth).has_first_order_rate()
    assert     reaction(rate=first).has_first_order_rate()
    assert not reaction(rate=second).has_first_order_rate()
    assert not reaction(rate=K_D).has_first_order_rate()

    assert not reaction(rate=zeroth).has_second_order_rate()
    assert not reaction(rate=first).has_second_order_rate()
    assert     reaction(rate=second).has_second_order_rate()
    assert not reaction(rate=K_D).has_second_order_rate()

    assert not reaction(rate=zeroth).has_equilibrium_dissociation_rate()
    assert not reaction(rate=first).has_equilibrium_dissociation_rate()
    assert not reaction(rate=second).has_equilibrium_dissociation_rate()
    assert     reaction(rate=K_D).has_equilibrium_dissociation_rate()

    assert not reaction(rate=1).has_zeroth_order_rate()
    assert not reaction(rate=1).has_first_order_rate()
    assert not reaction(rate=1).has_second_order_rate()
    assert not reaction(rate=1).has_equilibrium_dissociation_rate()

from multiset import multiset
import re
from infobiotics.commons.quantities import *
import config



# use http://re-try.appspot.com/ for live regex matching - use method 'match' and make sure 'VERBOSE' is on

rule_comment = """\s*(\#\s*(?P<comment>[ ,=+/*\?\-\^()"'\w\t]+)\s*\#??\s*)? # optional comment without new lines or '#' but including some math expressions with optional closing '#'"""

transformation_rule_matcher = re.compile("""
    # ' r1 : a + b [ c + d ]_l1 k1-> e + f [ g + h ]_l2     k2 = 0.1 '
    # ' r1 : (a+b|a + b [ c + d ]_l1) k1-> (e + f|e + f [ g + h ]_l2)     k2 = 0.1 '        
    \s*
    ((?P<rule_id>\w+)\s*\:)?                                   # r1:
    \s*
(
    (?P<reactants_outside>
    (\w+)                                                      # a
    (\s*\+\s*(\w+))*                                           # + b (+ ...)
    )?                                      
    \s*
    \[                                                         # [
    \s*
    (?P<reactants_inside>
    (\w+)                                                      # c
    (\s*\+\s*(\w+))*                                           # + d (+ ...)
    )?
    \s*
    \]                                                         # ]
    (_(?P<reactants_label>\w+))?                               # _l1
|                                                              # OR
    (?P<reactants>
    (\w+)                                                      # a
    (\s*\+\s*(\w+))*                                           # + b (+ ...)
    )?                                      
)
\s+ # whitespace (one or more times), so at least one space is required if there are no reactants (nothing to left of ->). This could be replaced with (?(reactants)\s*|\s+)? which doesn't need a space if there are no reactants but then we need a way to handle non-'-' prefixed rate/rate_id because '1->a' has 1 as a reactant.                                                        
-*                                                         # - (zero or more times)
(?P<rate_id>((\w+)|([+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?))?                                          # rate_id can nothing, a Python identifer or a number (int or float). Previous -* will greedily match away any '-' (minus) symbols
(-*>)                                              # - (zero or more times) followed by > # -> (once)
\s*
(
    (?P<products_outside>
    (\w+)                                                      # e
    (\s*\+\s*(\w+))*                                           # + f (+ ...)
    )?                                      
    \s*
    \[                                                         # ]
    \s*
    (?P<products_inside>
    (\w+)                                                      # g
    (\s*\+\s*(\w+))*                                           # + h (+ ...)
    )?                                      
    \s*
    \]                                                         # ]
    (_(?P<products_label>\w+))?                                # _l2
|
    (?P<products>
    (\w+)                                                      # a
    (\s*\+\s*(\w+))*                                           # + b (+ ...)
    )?                                      
)                             
    (                                                        
    \s+                                                        # whitespace (one or more times)
    (?(rate_id)(\w+)?|(?P<rate_id2>\w+))?                      # rate_id2 if rate_id not specified (optional and not greedy '??')
    (
    \s*
    \=*                                                         # zero or more =
    \s*
    [+]?(?P<rate>\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?            # 0.01 (any float or int), possibly preceeded but a '+' (plus) but never a '-' (minus)
    )?
    )?
""" + rule_comment, re.VERBOSE)


new_rate_regex = '''
\s*
(?P<rate>([-+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+\s*)?)
\s*
((?P<units>[*/]\s*[-+.\w]\s*[-+*/.\^\w\s]+)?)
\s*
0.1 * micromolar / hour
0.2 * micromolar
100 / hour
250 / micromolar / hour

n */ molar ** -1 * 


label = self.__regex.sub(r"\g<1>*\g<2>", label.replace('^', '**').replace('·', '*')) # from quantities.registry.__getitem__

'''


transport_rule_matcher = re.compile("""

# [ PQS ]_medium == ( 1, 0 ) == [   ] -1.0-> [   ]_medium = (  1, 0 ) = [PQS] d = 100   #visible #hidden
#   ___             ________           _____                                  _______
# PQS -> (1, 0) 0.1
# PQS -> (1, 0) x=0.1
# PQS 0.1-> (1, 0)
# PQS x-> (1, 0) x=0.1
# reaction('PQS -> (1,0)', rate=0.1)
# reaction('PQS x-> (1,0)', x=0.1)
# reaction('PQS -> (1,0)' x, x=0.1)
# reaction('PQS -> (1,0) x', x=0.1, rate=0.2)
  

    \s*
    ((?P<rule_id>\w+)\s*\:)? # nothing or 'r1:' or 'r_1' or 'r:' or 'r :' but not ':'
    \s*

\s*\[\s*(?P<reactant_here>(\w+))?\s*\](_(?P<reactant_label>\w+))? # reactant and label

\s*=+\s*\(\s*(?P<vector>[-]?\d+\s*,\s*[-]?\d+\s*)\)\s*=+\s*\[\s*\] # vector between one or more equals

\s+                                                        # whitespace (one or more times)
-*                                                         # - (zero or more times)
(?P<rate_id>((\w+)|([+]?\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?))?                                          # rate_id can be a Python identifer or a positive number (int or float). Previous -* will greedily match away any '-' (minus) symbols
(-*>)                                              # - (zero or more times) followed by > # -> (once)
\s*

\[\s*\](_(?P<reactant_label2>\w+))?
\s*=+\s*\(\s*(?P<vector2>[-]?\d+\s*,\s*[-]?\d+\s*)\)\s*=+\s*\[\s*(?P<product_there>(\w+))?\s*\]

    (                                                        
    \s+                                                        # whitespace (one or more times)
    (?(rate_id)(\w+)?|(?P<rate_id2>\w+))??                      # rate_id2 if rate_id not specified (optional and not greedy '??')
    (
    \s*
    \=*                                                         # zero or more =
    \s*
    [+]?(?P<rate>\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?            # 0.01 (any float or int), possibly preceeded but a '+' (plus) but never a '-' (minus)
    )?
    )?
""" + rule_comment, re.VERBOSE)

##TODO attempt to refactor regex as composed of smaller regexes - could use Meld for comparing transport_rule_matcher and transformation_rule_matcher strings
#
#one_whitespace = """\s # one whitespace"""
#zero_or_more_whitespace = """\s*"""
#one_or_more_whitespace = """\s+"""
#
#
#vector_between_one_or_more_equals = """\s*=+\s*\(\s*(?P<vector>[-]?\d+\s*,\s*[-]?\d+\s*)\)\s*=+\s*\[\s*\] # vector between one or more equals"""
#
#rule_id = """((?P<rule_id>\w+)\s*\:)? # nothing or 'r1:' or 'r_1' or 'r:' or 'r :' but not ':'"""
#
#one_species_and_label = """\s*\[\s*(?P<reactant_here>(\w+))?\s*\](_(?P<reactant_label>\w+))? # reactant and label"""

class reaction(object):

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()

    def repr(self, indent='\t', indent_level=0, id=''):
#        return "%s%s%sreaction(reactants_outside=%r, reactants_inside=%r, reactants_label='%s', products_outside=%r, products_inside=%r, products_label='%s', rate=%s)" % (indent, id, '=' if id != '' else '', self.reactants_outside, self.reactants_inside, self.reactants_label, self.products_outside, self.products_inside, self.products_label, self.rate)
        return "%s%s%sreaction('%s')" % (indent * indent_level, id, '=' if id != '' else '', self.str())

    def str(self, indent='', indent_level=0, comment=False):
#        return '%s%s: %s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s = %s' % (
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
            str(self.rate),
            '' if not comment or self.comment is None else '# %s #' % self.comment
        )

    def __init__(self, rule=None, rate=None, **kwargs):

        self.rule_id = None
        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = None
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = None
        self.rate_id = None
        self.rate_id2 = None
        self.rate = rate
        self.comment = None

        self.reactant_label = None
        self.reactant_here = multiset()
        self.vector = None
        self.reactant_label2 = None
        self.vector2 = None
        self.product_there = multiset()

        for k, v in kwargs.items(): setattr(self, k, v)

        if rule is not None:
            if not isinstance(rule, basestring):
                raise ValueError('rule is not a string: % s' % rule)
            self.create_reaction_from_rule(rule)

#        print repr(self.rate) #TODO rate - see infobiotics.commons.quantities.units.calculators:conversion_function_from_units
        if self.rate is None:
            raise ValueError("No rate could be determined for reaction%s." % " '%s'" % rule if rule is not None else '')

        #TODO needs testing
        if len(self.reactants_outside) > 2:
            raise ValueError("Rule ' % s' has too many reactants outside, a maximum of 2 reactants is permitted for any reaction." % self.str())
        elif len(self.reactants_inside) > 2:
            raise ValueError("Rule ' % s' has too many reactants inside %s, a maximum of 2 reactants is permitted for any reaction." % (self.str(), self.reactants_label))
        elif len(self.reactants_outside) + len(self.reactants_inside) > 2:
            raise ValueError("Rule ' % s' has too many reactants, a maximum of 2 reactants is permitted for any reaction." % self.str())

#    @classmethod #TODO ?
    def create_reaction_from_rule(self, rule):
        if transformation_rule_matcher.match(rule):
            match = transformation_rule_matcher.match(rule)
#            print 'here', match.groupdict()['rate']
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

        elif transport_rule_matcher.match(rule):
            match = transport_rule_matcher.match(rule)
            for name, value in match.groupdict().items():
                print name, value #TODO
                if name in ('reactant_label', 'reactant_label2'):
                    if value is not None:
                        pass
                elif name in ('vector', 'vector2'):
                    pass
                elif name in ('rate_id', 'rate_id2'):
                    pass
                elif name in ('reactant_here'):
                    pass
                elif name in ('product_there'):
                    pass
                elif name == 'rate':
                    pass
                elif name == 'rule_id': #TODO if value is None: use name in metacompartment and compartment
                    pass
                setattr(self, name, value)
            print
        else:
            raise ValueError("Failed to create reaction from rule '%s'.\nAll rules require at least one space before '->'." % rule) #TODO examples of valid rules

        # if self.rate is None
        # try and get rate from (in this order):
        #     rate group in rule, 
        #     rate metadata on reaction, # enables generic overriding
        #     metadata attribute with same name as rule_id on reaction
        # see test_reaction_rate.py  
        if self.rate is None and self.rate_id is not None:
            self.rate = self.rate_id

        # now convert to quantity or float

#        #TODO move below quantity parsing
#        if not isinstance(self.rate, Quantity):
#            if isinstance(self.rate, (int, float)):
#                self.rate = self.rate * config.time_units ** -1
#            else:
#                raise ValueError('...')

#        #TODO parse quantity using eval
#        print self.rate,
#        maybe_quantity = False
#        for ch in self.rate:
#            if ch in '':
#                maybe_quantity = True
#        try:
#            self.rate = eval(self.rate)
#            print self.rate
#        except Exception, e:
#            print 'eval exception', e

        if not isinstance(self.rate, Quantity):
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

    r1 = reaction('a -> b 5*10^-3 M^-1 s**-1')
    print r1

    r2 = reaction('a -> b', rate=5e-3 * M ** -1 * seconds ** -1)
    print r2

#    units = M ** -1 * seconds ** -1
#
#    rates = np.linspace(0, 1, 11)
#
#    for rate in rates:
#        print rate * units,
#        system = model(compartment(reaction('a -> b', rate=rate)))
#    print
#    print system

    exit()


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

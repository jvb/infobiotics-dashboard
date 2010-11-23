#from id_generators import id_generator
from multiset import multiset
import re

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
\s+                                                        # whitespace (one or more times)
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

transport_rule_matcher = re.compile("""

# [ PQS ]_medium == ( 1, 0 ) == [   ] -1.0-> [   ]_medium = (  1, 0 ) = [PQS] d = 100   #visible #hidden

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
#    _id_generator = id_generator('r')

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

        #TODO rate - see infobiotics.commons.quantities.units.calculators:conversion_function_from_units

        #TODO needs testing
        if len(self.reactants_outside) > 2:
            raise ValueError("Rule ' % s' has too many reactants outside, a maximum of 2 reactants is permitted for any reaction." % self.str())
        elif len(self.reactants_inside) > 2:
            raise ValueError("Rule ' % s' has too many reactants inside %s, a maximum of 2 reactants is permitted for any reaction." % (self.str(), self.reactants_label))
        elif len(self.reactants_outside) + len(self.reactants_inside) > 2:
            raise ValueError("Rule ' % s' has too many reactants, a maximum of 2 reactants is permitted for any reaction." % self.str())


    def create_reaction_from_rule(self, rule):
        if transformation_rule_matcher.match(rule):
            match = transformation_rule_matcher.match(rule)
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
                    elif value is not None:
                        value = float(value)
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
            raise ValueError('Failed to create reaction from rule "%s".' % rule)

        # if self.rate is None
        # try and get rate from (in this order):
        #     rate group in rule, 
        #     rate metadata on reaction, 
        #     metadata attribute with same name as rule_id on reaction
        # see test_reaction_rate.py  
        if self.rate is None and self.rate_id is not None:
            try:
                self.rate = float(self.rate_id)
                self.rate_id = 'c' # since rate_id is number we should make it a generic label
            except ValueError:
                try:
                    self.rate = float(getattr(self, self.rate_id))
                except ValueError, e: # float conversion failed
                    raise ValueError("Couldn't assign a rate with id '%s' from metadata: %s" % (self.rate_id, e))
                except AttributeError, e: # no attribute with name rate_id
                    raise AttributeError("Couldn't assign a rate with id '%s' from metadata: %s" % (self.rate_id, e))

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()

    def repr(self, indent='', id=''):
#        return "%s%s%sreaction(reactants_outside=%r, reactants_inside=%r, reactants_label='%s', products_outside=%r, products_inside=%r, products_label='%s', rate=%s)" % (indent, id, '=' if id != '' else '', self.reactants_outside, self.reactants_inside, self.reactants_label, self.products_outside, self.products_inside, self.products_label, self.rate)
        return "%s%s%sreaction('%s')" % (indent, id, '=' if id != '' else '', self.str())

    def str(self, indent='', comment=False):
#        return indent + '%s: %s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s = %s' % (
#            self.id,
        return indent + '%s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s=%f %s' % (
            self.reactants_outside,
            ' ' if len(self.reactants_outside) > 0 else '',
            self.reactants_inside,
            self.reactants_label,
            self.rate_id,
            self.products_outside,
            ' ' if len(self.products_outside) > 0 else '',
            self.products_inside,
            self.products_label,
            self.rate_id,
            self.rate,
            '' if not comment or self.comment is None else '# %s #' % self.comment
        )
        

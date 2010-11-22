from base import base
from id_generators import id_generator
from multiset import multiset
import re, sys

rule_matcher = re.compile('''
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
    \s*
    \]                                                         # ]
    (_(?P<reactants_label>\w+))?                               # _l1
|
    (?P<reactants>
    (\w+)                                                      # a
    (\s*\+\s*(\w+))*                                           # + b (+ ...)
    )?                                      
)
    \s+                                                        # whitespace (one or more times)
    -*                                                         # - (zero or more times)
    (?P<rate_id>\w+)?                                          # k1 **
    (->){1}                                                    # -> (once)
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
    \s+                                                        # whitespace (one or more times)
    (?(rate_id)(\w+)?|(?P<rate_id2>\w+))                       # rate_id2 if rate_id not specified
    \s*
    \=                                                         # =
    \s*
    [-+]?(?P<rate>\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?            # 0.01 (any float or int)
    \s*        
''', re.VERBOSE)

class reaction(base):
    _id_generator = id_generator('r')

    def create_reaction_from_rule(self, rule):
        match = rule_matcher.match(rule)
        if match is None:
            raise ValueError('Failed to create reaction from rule "%s".' % rule)
        reactants_set = False
        products_set = False
        for name, value in match.groupdict().items():
            if name in ('reactants_outside', 'reactants_inside',
                        'products_outside', 'products_inside',
                        'reactants', 'products',
            ):
                # reactants or products are specified only when '[ ]' missing
                if name == 'reactants':
                    reactants_set = True
                elif name == 'products':
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
                    value = multiset([s.strip() for s in value.split('+')]) # can construct multiset from a list of str where the same str value might appear more than once
                else:
                    value = multiset()
            elif name == 'rate_id':
                if value is None:
                    continue # don't overwrite value from rate_id if already set
            elif name == 'rate_id2':
                if match.groupdict()['rate_id'] is None:
                    if value is None:
                        raise ValueError('rate_id2 ignored if rate_id set otherwise mandatory')
                    name = 'rate_id'
            #TODO reactants_label, products_label
            setattr(self, name, value)

    def __init__(self, rule=None, **kwargs):

        self.rule_id = None
        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = 'l'
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = 'l'
        self.rate_id = 'k'
        self.rate = 0

        for k, v in kwargs.items(): setattr(self, k, v)

        if rule is not None:
            if isinstance(rule, basestring):
                self.create_reaction_from_rule(rule)
            else:
                raise ValueError('rule is not a string: %s' % rule)

        #TODO rate - see infobiotics.commons.quantities.units.calculators:conversion_function_from_units

        #TODO needs testing
        if len(self.reactants_outside) > 2:
            raise ValueError("Rule '%s' has too many reactants outside, a maximum of 2 reactants is permitted for any reaction." % self.str())
        elif len(self.reactants_inside) > 2:
            raise ValueError("Rule '%s' has too many reactants inside %s, a maximum of 2 reactants is permitted for any reaction." % (self.str(), self.reactants_label))
        elif len(self.reactants_outside) + len(self.reactants_inside) > 2:
            raise ValueError("Rule '%s' has too many reactants, a maximum of 2 reactants is permitted for any reaction." % self.str())

#        # must be after base.__init__ as id not set otherwise 
#        if self.rule_id is not None: #TODO remove, use rule_id for name instead of generating one
#            sys.stderr.write("Rule id '%s' of the rule '%s: %s' will not be used internally, instead the id '%s' will be used as it is guaranteed to be globally unique.\n" % (self.rule_id, self.rule_id, self.str(), self.id))

    def str(self, indent=''):
#        return indent + '%s: %s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s = %s' % (
#            self.id,
        return indent + '%s%s[ %s ]_%s -%s-> %s%s[ %s ]_%s %s = %s' % (
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
        )

    def repr(self, indent=''):
#        return indent + "reaction('%s')" % self.str()
#        decl = '' if self._named else '%s=%s' % (self.id, self.__class__.__name__ if self.__class__.__name__ != 'species' else '')
#        return indent + "'%s'" % self.str()
        return "reaction(reactants_outside=%s, reactants_inside=%s, reactants_label='%s', products_outside=%s, products_inside=%s, products_label='%s', rate_id='%s', rate=%s)" % (self.reactants_outside, self.reactants_inside, self.reactants_label, self.products_outside, self.products_inside, self.products_label, self.rate_id, self.rate)


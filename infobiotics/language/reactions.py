from base import base
from id_generators import reaction_id_generator
from multiset import multiset
import re, sys


class reaction(base):
    _id_generator = reaction_id_generator

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
|
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
    
    def __init__(self, reaction=None, **kwargs):

        self.rule_id = None
        self.reactants_outside = multiset()
        self.reactants_inside = multiset()
        self.reactants_label = 'l' #TODO compartment
        self.products_outside = multiset()
        self.products_inside = multiset()
        self.products_label = 'l' #TODO compartment
        self.rate_id = 'k'
        self.rate = 0

        # overwrite above with kwargs
        base.__init__(self, **kwargs)

        if reaction is not None:
            if isinstance(reaction, str):
                # attempt regex
                match = self.rule_matcher.match(reaction)
                if match is not None:
                    match_groups_dict = match.groupdict()
                    for name, value in match_groups_dict.items():
                        if name == 'rule_id':
                            self.rule_id = value
                        elif name in ('reactants_outside', 'reactants_inside', 'products_outside', 'products_inside', 'reactants', 'products'):

                            # reactants or products are specified only when '[ ]_l' is missing
                            if name == 'reactants':
                                name = 'reactants_inside'
                            elif name == 'products':
                                name = 'products_inside'
                            
                            if value is not None:
                                setattr(self, name, multiset([s.strip() for s in value.split('+')])) # can construct multiset from a list of str where the same str value might appear more than once
                            else:
                                setattr(self, name, multiset())
                        
                        # rate_id2 ignored if rate_id set otherwise mandatory
                        elif name == 'rate_id':
                            if value is not None:
                                self.rate_id = value
                        elif name == 'rate_id2':
                            if match_groups_dict['rate_id'] is None:
                                self.rate_id = value
                                
                        else:
                            setattr(self, name, value)
                else:
                    print 'Failed to create reaction from "%s"' % reaction

        #TODO rate - see infobiotics.commons.quantities.units.calculators:conversion_function_from_units

        #TODO needs testing
        if len(self.reactants_outside) > 2:
            raise ValueError("Rule '%s' has too many reactants outside, a maximum of 2 reactants is permitted for any reaction." % self.str())
        elif len(self.reactants_inside) > 2:
            raise ValueError("Rule '%s' has too many reactants inside %s, a maximum of 2 reactants is permitted for any reaction." % (self.str(), self.reactants_label))
        elif len(self.reactants_outside) + len(self.reactants_inside) > 2:
            raise ValueError("Rule '%s' has too many reactants, a maximum of 2 reactants is permitted for any reaction." % self.str())

        # must be after base.__init__ as id not set otherwise 
        if self.rule_id is not None:
            sys.stderr.write("Rule id '%s' of the rule '%s: %s' will not be used internally, instead the id '%s' will be used as it is guaranteed to be globally unique.\n" % (self.rule_id, self.rule_id, self.str(), self.id))

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
        decl = '' if self._named else '%s=%s' % (self.id, self.__class__.__name__ if self.__class__.__name__ != 'species' else '')
        return indent + "'%s'" % self.str()


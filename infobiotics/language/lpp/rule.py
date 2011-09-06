from enthought.traits.api import HasTraits, DictStrInt, Str, Float, Enum

class Rule(HasTraits):
    reactantsOutside = DictStrInt
    reactantsInside = DictStrInt 
    reactantslabel = Str 
    productsOutside = DictStrInt 
    productsInside = DictStrInt
    productsLabel = Str
    constant=Float
#    constant_units = Enum(['molecules second^-1','molecules minute^-1', 'molecules hour^-1'])

    def __str__(self):
        s = ''
        s += objects_dict_to_str(self.reactantsOutside) 
        s += ' ' if len(self.reactantsOutside) > 0 else ''
        s += '[ '
        s += objects_dict_to_str(self.reactantsInside)
        s += ' ]_'
        s += self.productsLabel
        s += ' '
        s += '-'
        s += str(self.constant)
        s += '-> '
        s += objects_dict_to_str(self.productsOutside) 
        s += ' ' if len(self.productsOutside) > 0 else ''
        s += '[ '
        s += objects_dict_to_str(self.productsInside)
        s += ' ]_'
        s += self.productsLabel
##        s += ';'
#        s += ' '
#        s += '('
#        s += str(self.constant)
#        s += ')'
        return s
    
def objects_dict_to_str(d):
    ''' Returns 'a + b + b' given {'a':1,'b':2}. '''
    return ' + '.join([k for k, v in d.iteritems() for _ in range(v)])

def objects_str_to_dict(s):
    objects = s.replace(' ', '').split('+')
    return dict([(object, objects.count(object)) for object in objects])

def rule_str_to_Rule(s):
    ''' Returns Rule given 'a + b + b [ c + d ]_l -0.1-> e + f + g [ h ]_l2' '''
    lc, r = s.split('->')
    l, c = lc.rsplit('-', 1)
    loli, ll = l.rsplit('_', 1)
    reactantsLabel = ll.strip()
    lo, li = loli.strip(']').split('[')
    reactantsOutside = objects_str_to_dict(lo)
    reactantsInside = objects_str_to_dict(li)
    rori, rl = r.rsplit('_', 1)
    productsLabel = rl.strip()
    ro, ri = rori.strip(']').split('[')
    productsOutside = objects_str_to_dict(ro)
    productsInside = objects_str_to_dict(ri)
    constant = float(c.strip())
    return Rule(
        reactantsOutside=reactantsOutside,
        reactantsInside=reactantsInside, 
        reactantslabel=reactantsLabel,
        productsOutside=productsOutside, 
        productsInside=productsInside,
        productsLabel=productsLabel,
        constant=constant,
    )

def rule(s):
    return rule_str_to_Rule(s)

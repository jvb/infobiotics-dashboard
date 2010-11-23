import unittest2 as unittest
from infobiotics.language.compartments import *

class TestReaction(unittest.TestCase):

    def test_regex(self):

        def match(rule):
            ''' Returns None is match not found. '''
            return reaction.rule_matcher.match(rule)
        
        def good(rule):
            self.assertNotEqual(match(rule), None)

        def bad(rule):
            self.assertEqual(match(rule), None)

        good('[ a ]_bacteria k-> [ b ]_bacteria k=0.1')
        good('[ a ] k-> [ b ] k=0.1')
        good('a k-> b k=0.1')
        good('[ a ]_bacteria k-> [ b ]_bacteria k=0.1') 
        
        bad('[ a ] k-> [ b ]_bacteria k=0.1')
        bad('[ a ] k-> [ b ] k=0.1')
        bad('a []_l k-> b k=0.1')
        bad('[ a ]_bacteria -> [ b ]_bacteria =0.1') # not rate_id 
        bad(' a ]_bacteria k-> [ b ]_bacteria k=0.1')
         

class TestSpecies(unittest.TestCase):

    def test(self):
        pass
    


#def setitem(object, name, value):
#    ''' Needed because assertRaises requires a callable. '''
#    object[name] = value

class TestCompartment(unittest.TestCase):

    def test_class_setattr(self):
        class c(compartment):
            a = 5
#            f = 5.1 #TODO either prints a warning or not and sets the attribute
#            d = {'a':5, 'b':1} #TODO
#            pass
        self.assertIsInstance(c.a, species)
        self.assertEqual(c.a.name, 'a')
        self.assertEqual(c.a.amount, 5)
        self.assertEqual(c.a.amount, 5 * molecule)

    def test_class_setattr_private(self):
        class c(compartment):
            _a = 5
        self.assertIsInstance(c._a, int)
        self.assertEqual(c._a, 5)
        pass

    def test_instance_setattr_private(self):
        pass

    def test_instance_getitem(self):
        c = compartment()
        self.assertEqual(c['a'], None)

#    def test_instance_setitem(self):
#        c = compartment()
#        c['a'] = 1 # == setitem(c, 'a', 1)
#        self.assertEqual(c['a'].amount, 1)

    def test_readonly_properties(self):
        c = compartment()
        for property_name in ('compartments', 'species', 'reactions'):
            self.assertRaises(AttributeError, setattr, c, property_name, None)
#            self.assertRaises(AttributeError, setitem, c, property_name, None)


    def test_instance_setattr(self):
        c = compartment() # instance

        # volume

        self.assertEqual(c.volume, 1) # default value

        c.volume = 2 * metre ** 3 # accepted
        self.assertEqual(c.volume, 2)

        c.volume = 2 # converted to m ** 3
        self.assertEqual(c.volume, 2)

        self.assertRaises(ValueError, setattr, c, 'volume', 2 * mM)

        self.assertRaises(ValueError, setattr, c, 'volume', 2 * metre ** 2)

        self.assertRaises(AttributeError, getattr, c, 'a')

        # a species

        c.a = 1 * millimoles # accepted, is__concentration == False
        self.assertIsInstance(c.a, species)
        self.assertEqual(c.a.name, 'a')
        self.assertEqual(c.a.amount, 1)
        self.assertEqual(c.a._concentration, False)

        c.a = 1 * nanomolar # accepted, is__concentration == True
        self.assertIsInstance(c.a, species)
        self.assertEqual(c.a.name, 'a')
        self.assertEqual(c.a.amount, 1)
        self.assertEqual(c.a._concentration, True)

        c.a = 1 * molecule # accepted, is__concentration == False
        self.assertIsInstance(c.a, species)
        self.assertEqual(c.a.name, 'a')
        self.assertEqual(c.a.amount, 1)
        self.assertEqual(c.a._concentration, False)

        c.a = 1 # converted to molecules
        self.assertIsInstance(c.a, species)
        self.assertEqual(c.a.name, 'a')
        self.assertEqual(c.a.amount, 1)

        self.assertRaises(ValueError, setattr, c, 'a', 1 * mL)

#        self.assertRaises(ValueError, setattr, c, 'f', 0.1)
        

if __name__ == '__main__':
    unittest.main()


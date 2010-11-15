import unittest2 as unittest
from infobiotics.language import *
from enthought.traits.api import TraitError

def setitem(object, name, value):
    ''' Needed because assertRaises requires a callable. '''
    object[name] = value

class TestCompartment(unittest.TestCase):

    def test_class_Int(self):
        class C(compartment):
            a = 5
        self.assertIsInstance(C.a, species)

    def test_private_Int(self):
        class C(compartment):
            _a = 5
        self.assertIsInstance(C._a, int)

    def test_instance_Int(self):
        c = compartment()
        c.a = 6
        self.assertIsInstance(c.a, species)
        self.assertEqual(c.a.id, 'a')

    def test_class_DictStrInt(self):
        class C(compartment):
            d = {'a':5, 'b':1}
        self.assertEqual(C.a, 5)
        self.assertEqual(C.b, 1)

    def test_mapping_access(self):
        c = compartment()
        c['a'] = 1 # == setitem(c, 'a', 1)
        self.assertEqual(c['a'].amount, 1)

    def test_readonly_properties(self):
        c = compartment()
        for property, value in (('compartments', [compartment()]), ('species', [species()]), ('reactions', [reaction()])):
            self.assertRaises(TraitError, setattr, c, property, value)
            self.assertRaises(TraitError, setitem, c, property, value)


if __name__ == '__main__':
    unittest.main()


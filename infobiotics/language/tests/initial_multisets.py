import unittest2 as unittest
from infobiotics.language import *

class TestInitialAmounts(unittest.TestCase):

    def setUp(self):
        class Compartment(compartment):
            a = species(1)
        self.c = Compartment()

    def testClassSpecies(self):
        for a in (self.c.a, self.c['a']):
            self.assertIsInstance(a, species)
            self.assertEqual(a.quantity, 1)
            self.assertEqual(str(a), '1')

    def testClassDictStrInt(self):
        ''' Adding DictStrInt (multiset) to compartment objects updates species
        amounts, creating new species with id str if not present already. '''
        self.c.initial_amounts = {'a':10, 'b':2}
        for a in (self.c.a, self.c['a']):
            self.assertIsInstance(a, species)
            self.assertEqual(a.quantity, 10)
            self.assertEqual(str(a), '10')
        for b in (self.c.b, self.c['b']):
            self.assertIsInstance(b, species)
            self.assertEqual(b.quantity, 2)
            self.assertEqual(self.c.quantity('b'), '2')


if __name__ == '__main__':
    unittest.main()

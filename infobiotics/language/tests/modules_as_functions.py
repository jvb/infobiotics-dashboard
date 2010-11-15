import unittest2 as unittest
from infobiotics.language import *

## modules
#
#def module(var, var_with_default='a'): #TODO
#    r1 = reaction(products=var)
#    r2 = reaction(reactants=var_with_default)
#    return r1, r2
#
#class HasModule(compartment):
#    module1 = module('b')
#c = HasModule()
#print c._reactions() #TODO look inside tuples for reactions
#exit()

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test1(self):
        self.assertEqual(True, True)

    def test2(self):
        self.assertNotEqual(True, False)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

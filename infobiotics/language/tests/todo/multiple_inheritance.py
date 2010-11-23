## multiple inheritance
#
#class c1(compartment):
#    x = compartment(name='1')
#    a = species(1)
#    b = reaction()
#    c = species(3)
#
#class c2(compartment):
#    x = compartment(name='2')
#    c = species(2)
#
#class C(c2, c1):
#    pass
#
#c = C()
#assert c.c.quantity == 2 # c in C2 overrides c in C1
##print [i.name for i in c._compartments()]
##print [str(i) for i in c._species()]
##print [i.name for i in c._reactions()]

import unittest2 as unittest
from infobiotics.language import *

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

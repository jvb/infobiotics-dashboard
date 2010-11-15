import unittest2 as unittest
from infobiotics.language import *

## knockout as subclass of wildtype
#class WildType(compartment):
#    species_rsmA = 1
#class rsmAKnockout(WildType):
#    species_rsmA = 0
#
#

#sps = compartment
#SpatialDistribution = np.array
#
#class model1(lpp):
#    distribution = SpatialDistribution([[rsmAKnockout() if (x == 4 and y == 4) else WildType() for x in range(10)] for y in range(10)])
#
#m = model()
##print m.distribution
#print m.distribution[4, 4]
#m.distribution[4, 4] = None
#print m.empty_positions()


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

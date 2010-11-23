# remove bad chars, trailing line feeds, etc. 

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

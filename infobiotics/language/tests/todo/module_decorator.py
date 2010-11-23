import unittest2 as unittest
from infobiotics.language.module_decorator import module

class Test(unittest.TestCase):

    def setUp(self):
        self.nested = ['a', ['b', ('c',), ['d'], ], ['e']]

    def test_unflattened(self):
        def unflattened():
            return self.nested
        self.assertNotEqual(len(unflattened()), 5)

    def test_flattened(self):
        @module
        def flattened():
            return self.nested
        self.assertEqual(len(flattened()), 5)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()






import unittest2
from infobiotics.language.reactions import reaction

class TestReactionRateDetermination(unittest2.TestCase):
    
    # normal
    
    def test_no_rule_id_or_equals(self):
        ''' Zero or many equals and no rule id, it doesn't matter as long as there is a rate'''
        r = reaction('a -> b 4')
        self.assertEqual(r.rate, 4)
        r = reaction('a -> b =4')
        self.assertEqual(r.rate, 4)
        r = reaction('a -> b ==4')
        self.assertEqual(r.rate, 4)
        r = reaction('[a] -> [b] 4')
        self.assertEqual(r.rate, 4)
        r = reaction('[a]_l -> [b]_l 4')
        self.assertEqual(r.rate, 4)
    
    def test_both_rule_ids_matching(self):
        ''' Rate used with rule ids and equals '''
        r = reaction('a x-> b x=4')
        self.assertEqual(r.rate, 4)

    def test_both_rule_ids_nonmatching(self):
        ''' Rate used even if rule ids don't match. ''' #TODO not a feature, possibly a bug?
        r = reaction('a x-> b y=4')
        self.assertEqual(r.rate, 4)

    def test_rule_id_is_rate(self):
        r = reaction('a 4-> b')
        self.assertEqual(r.rate, 4)

    def test_rule_id_is_rate_float(self):
        r = reaction('a 4.0-> b')
        self.assertEqual(r.rate, 4)

    def test_rule_id_metadata_used_for_rate(self):
        r = reaction('a x-> b', x=4)
        self.assertEqual(r.rate, 4)

    def test_rule_id_metadata_used_for_rate2(self):
        ''' Rule id in place of rate uses metadata for rate. '''
        r = reaction('a -> b x', x=4)
        self.assertEqual(r.rate, 4)

    def test_rate_metadata_overrides_rule_id_metadata(self):
        r = reaction('a x-> b', x=4, rate=5)
        self.assertEqual(r.rate, 5)

    def test_rate_metadata_used_for_rate(self):
        r = reaction('a x-> b', rate=5)
        self.assertEqual(r.rate, 5)

    # pathlogical

    def test_rule_id_but_no_rate(self):
        ''' Rule id without rate needs metadata. '''
        self.assertRaises(AttributeError, reaction, 'a x-> b')
        self.assertRaises(AttributeError, reaction, 'a -> b x=')

    def test_rule_id_but_no_rate2(self):
        ''' Rule id used in place of rate needs metadata. '''
        self.assertRaises(AttributeError, reaction, 'a -> b x')
    
    def test_rule_id_metadata_used_for_rate_but_wrong_type(self):
        ''' Rule id used in place of rate needs valid metadata. '''
        self.assertRaises(ValueError, reaction, 'a -> b x', x='p')
    

if __name__ == '__main__':
    unittest2.main()      

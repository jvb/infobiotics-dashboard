from compartments import compartment         

class one(compartment):
    a = 1
    b = 1
    s = 'test'
        
    
class two(one):
    a = 2

two.c = 3

o = one()
o.d = 4
t = two()
t.e = 5

#for attr in ('species', 'reactions', 'compartments'):
#    print getattr(one, attr)
#    print getattr(two, attr)
#    print getattr(one(), attr)
#    print getattr(two(), attr)
#    print getattr(o, attr)
#    print getattr(t, attr)

metadata = {
#    's':'test',
#    's':'best',
#    'a':1,
#    'a':2, # didn't catch two.a - because two.a is a species
    'amount':lambda x: x > 2, # didn't catch two.c
}
print one.species(**metadata)
print two.species(**metadata)
print one().species(**metadata)
print two().species(**metadata)
print o.species(**metadata)
print t.species(**metadata)

#TODO reuse compartments(**metadata) from compartmentsmixin in model - but make it recursive

from id_generators import species_id_generator

class species(object):

    def __init__(self, amount=0, name=None):
        self.amount = amount
        self.id = species_id_generator.next()
        if name is not None:
            self.name = name
        else:
            self.name = self.id
    def __get__(self, obj, objtype=None):
#        print obj, object
        return self.amount
    def __set__(self, obj, value):
        self.amount = value

s = species()
print type(s), s
print s.id, s.amount
s = 1
print type(s), s
#print s.id, s.amount

class compartment(object):
    s = species()

c = compartment()
print type(c.s), c.s
print c.s.id, c.s.amount


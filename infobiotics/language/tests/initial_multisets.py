from infobiotics.language.api import compartment, species, reaction

class Compartment(compartment):
    a = species(1)
    b = species(2)
    amounts = {'a':10, 'b':0} # multiset()

c = Compartment()
print c.amounts
c.test = {'a':reaction()}
print c.test
print [(s.id, s) for s in c._species()]

exit()

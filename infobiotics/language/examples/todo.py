from infobiotics.language import *
print dir()

def module():
    r1 = reaction
    return r1

c = compartment(
    a=1,
    b=2,
    c=compartment(
        a=3,
    ),
    module1=module(),
    r1=reaction(),
    r2=reaction(),
)

print c

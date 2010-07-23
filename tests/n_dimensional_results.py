import numpy as np

n = 2

print '1 variable:'
print 'x Result'
#a = np.linspace(0, 1000, n).reshape((n,))
a = np.random.binomial(100,0.1,n).reshape((n,))
a = np.arange()
for xi, x in enumerate(np.linspace(0, 100, n)):
    print x, a[xi] 
print

print '2 variables:'
print 'x y Result'
#a = np.linspace(0, 1000, n**2).reshape((n,n))
a = np.random.binomial(100,0.1,n**2).reshape((n,n))
for xi, x in enumerate(np.linspace(0, 100, n)):
    for yi, y in enumerate(np.linspace(0, 10, n)):
        print x, y, a[xi,yi] 
print

print '3 variables:'
print 'x y z Result'
#a = np.linspace(0, 1000, n**3).reshape((n,n,n))
a = np.random.binomial(100,0.1,n**3).reshape((n,n,n))
for xi, x in enumerate(np.linspace(0, 100, n)):
    for yi, y in enumerate(np.linspace(0, 10, n)):
        for zi, z in enumerate(np.linspace(0, 2, n)):
            print x, y, z, a[xi,yi,zi] 
print

print '4 variables:'
print 'x y z w Result'
#a = np.linspace(0, 1000, n**4).reshape((n,n,n,n))
a = np.random.binomial(100,0.1,n**4).reshape((n,n,n,n))
for xi, x in enumerate(np.linspace(0, 100, n)):
    for yi, y in enumerate(np.linspace(0, 10, n)):
        for zi, z in enumerate(np.linspace(0, 2, n)):
            for wi, w in enumerate(np.linspace(0, 66.6, n)):
                print x, y, z, w, a[xi,yi,zi,wi] 
print

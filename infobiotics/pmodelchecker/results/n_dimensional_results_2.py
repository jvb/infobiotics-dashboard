import numpy as np

x = np.arange(0, 1.1111, 0.5555)
y = range(3)
z = range(4)
w = range(1)

print '1 variable:'
print 'x Result'
a = np.arange(len(x))
for xi, xd in enumerate(x):
    print xd, a[xi]
print

print '2 variables:'
print 'x y Result'
a = np.arange(len(x)*len(y)).reshape((len(x),len(y)))
for xi, xd in enumerate(x):
    for yi, yd in enumerate(y):
        print xd, yd, a[xi,yi]
print

print '3 variables:'
print 'x y z Result'
a = np.arange(len(x)*len(y)*len(z)).reshape((len(x),len(y),len(z)))
for xi, xd in enumerate(x):
    for yi, yd in enumerate(y):
        for zi, zd in enumerate(z):
            print xd, yd, zd, a[xi,yi,zi]
print

print '4 variables:'
print 'x y z w Result'
a = np.arange(len(x)*len(y)*len(z)*len(w)).reshape((len(x),len(y),len(z),len(w)))
for xi, xd in enumerate(x):
    for yi, yd in enumerate(y):
        for zi, zd in enumerate(z):
            for wi, wd in enumerate(w):
                print xd, yd, zd, wd, a[xi,yi,zi,wi]
print

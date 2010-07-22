import numpy as np
from math import sin, cos, tan

x = np.linspace(-4, 4, 100)
y = np.linspace(-4, 4, 100)
z = np.linspace(-4, 4, 10)
w = np.linspace(-4, 4, 10)
u = np.linspace(-4, 4, 10)

#print '1 variable:'
#print 'x Result'
#a = np.arange(len(x))
#for xi, xd in enumerate(x):
#    print xd, a[xi]
#print

print '2 variables:'
print 'x y Result'
a = np.arange(len(x)*len(y)).reshape((len(x),len(y)))
for xi, xd in enumerate(x):
    for yi, yd in enumerate(y):
#        print xd, yd, a[xi,yi]
        print xd, yd, sin(xd**2) * cos(yd**2)
print

#print '5 variables:'
#print 'x y z w u Result'
#a = np.arange(len(x)*len(y)).reshape((len(x),len(y)))
#for xi, xd in enumerate(x):
#    for yi, yd in enumerate(y):
#        for zi, zd in enumerate(z):
#            for wi, wd in enumerate(w):
#                for ui, ud in enumerate(u):
#                    print xd, yd, zd, wd, ud, sin(xd**2) * cos(yd**2) * cos(zd) * sin(wd) * tan(ud)
#print
#
#v = [x, y]
#for var in v:
    


#print '3 variables:'
#print 'x y z Result'
#a = np.arange(len(x)*len(y)*len(z)).reshape((len(x),len(y),len(z)))
#for xi, xd in enumerate(x):
#    for yi, yd in enumerate(y):
#        for zi, zd in enumerate(z):
#            print xd, yd, zd, a[xi,yi,zi]
#print

#print '4 variables:'
#print 'x y z w Result'
#a = np.arange(len(x)*len(y)*len(z)*len(w)).reshape((len(x),len(y),len(z),len(w)))
#for xi, xd in enumerate(x):
#    for yi, yd in enumerate(y):
#        for zi, zd in enumerate(z):
#            for wi, wd in enumerate(w):
#                print xd, yd, zd, wd, a[xi,yi,zi,wi]
#print

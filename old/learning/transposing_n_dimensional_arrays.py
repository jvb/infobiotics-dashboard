import numpy as np

x = range(2)
y = range(3)
z = range(4)
w = range(1)

#print '4 variables:'
#print 'x y z w Result'
a = np.arange(len(x)*len(y)*len(z)*len(w)).reshape((len(x),len(y),len(z),len(w)))
#for xi, xd in enumerate(x):
#    for yi, yd in enumerate(y):
#        for zi, zd in enumerate(z):
#            for wi, wd in enumerate(w):
#                print xd, yd, zd, wd, a[xi,yi,zi,wi]
#print

#print a '\n'

#for b in (
#    a[:,0,0,:],
##    a[:,0,0,:],
##    a[:,0,1,:],
##    a[:,:,0,0],
##    a[:,:,1,0],
##    a[:,0,:,0],
##    a[:,1,:,0],
##    a[0,:,:,0],
##    a[1,:,:,0],
#):
#    print b
#    print b.shape
#    print b.T
#    print b.T.shape
#    print b.swapaxes(0,1) 
#    print b.swapaxes(0,1).shape
#    print
    
#print a[1,:,:,0]
#print a[1,:,:,0].shape
#print a[1,:,:,0].T
#print a[1,:,:,0].T.shape
print a
print a.shape
print
#print a.T.shape
print a.transpose(3,1,2,0)
print a.transpose(3,1,2,0).shape
print a.swapaxes(3,0).shape
print
print a.swapaxes(3,0)[0,:,:,1]
print a[1,:,:,0].transpose()



#for isAxis in (True, False):
#    s += ':' if isAxis else xi 
#    s += ',' if i < 4 else ''
    
#for xi, xd in enumerate(x):
#    for yi, yd in enumerate(y):
#        for zi, zd in enumerate(z):
#            for wi, wd in enumerate(w):
##                print xd, yd, zd, wd, a[xi,yi,zi,wi]
#                s = ''
#                s += ':' if variable.name == self.xAxis or variable.name == self.yAxis else str(variable.valueIndex)
#                s += ',' if i != len(self.variables) - 1 else ''
#                print s

#for xi, xd in enumerate(x):
#    s = ''
#    for isAxis in (True, False):
#        s += ':' if isAxis else str(xi) 
#        s += ','
#        print 1
#        for yi, yd in enumerate(y):
#            for isAxis in (True, False):
#                s += ':' if isAxis else str(yi) 
#                s += ','
#                print 2
#                for zi, zd in enumerate(z):
#                    for isAxis in (True, False):
#                        s += ':' if isAxis else str(zi) 
#                        s += ','
#                        print 3
#                        for wi, wd in enumerate(w):
#                            for isAxis in (True, False):
#                                s += ':' if isAxis else str(wi)
#                                print 4
#                                print s

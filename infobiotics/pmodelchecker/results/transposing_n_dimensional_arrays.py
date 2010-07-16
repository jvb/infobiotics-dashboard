import numpy as np

n = 2

#a = np.arange(n**2).reshape((n,n))
a = np.arange(n**3).reshape((n,n,n))
#a = np.arange(n**4).reshape((n,n,n,n))

print 'a'
print a
print

print 'a.transpose()'
print a.transpose()
print

print 'a.transpose([2,1,0])'
print a.transpose([2,1,0])
print

print 'a.transpose([1,2,0])'
print a.transpose([1,2,0])
print

print 'a.transpose([0,2,1])'
print a.transpose([0,2,1])
print


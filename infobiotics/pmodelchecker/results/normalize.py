import numpy as np

a = np.array(
    [[[0, 0],
      [3, 5],
      [9, 9]],
     [[0, 0],
      [3, 5],
      [9, 9]],
     [[0, 0],
      [3, 5],
      [9, 9]]],
    dtype=np.float32,
)

b = np.arange(-10, 20)
print b

#print a[:,1,:]
#
#def normalize(value, maximum, minimum, scale=1):
#    return ((value - minimum) / (maximum - minimum)) * scale

def normalize_array(a):
    return a * (1 / (np.max(a) - np.min(a)))
#print normalize_array(a)

def normalize_array_by_other_array(a, other): # works!
    min = np.min(other)
    return (a - min) * 1 / (np.max(other) - min)
    # brackets are vital here because only '(a - min)' returns an array

print normalize_array_by_other_array(a, b)


'''

  1 8 4
2 7 7 7 5
2 7 7 7 5
  3 8 6

  1 8 4
2 7 7 7 5
2 7 7 7 5 1 8 4
  3 8 6 2 7 7 7 5
  1 8 4 2 7 7 7 5
2 7 7 7 5 3 8 6
2 7 7 7 5
  3 8 6


'<compartment metaid="c27" id="c27" name="z:::4,0" size="1" units="volume" outside="default"><annotation/></compartment>'

'''

#def id_generator(prefix='', initial=1):
#    i = initial
#    while True:
#        yield '%s%s' % (prefix, i)
#        i += 1
#
#compartment_id_generator = id_generator('c', initial=9)

import numpy as np


def print_distribution(distribution):
    print distribution.shape
    for y in distribution:
        for x in y:
            print x,
        print

width = 5
height = 4
#width = 20
#height = 20

a = 0
b = 0

pattern_width = 5
pattern_height = 4

def compartment_factory(x, y):
    if (x == a % width or x == (a + 4) % width) and (y == b % height or y == (b + 3) % height):
        return 0
    elif x == (a + 1) % width and y == b % height:
        return 1
    elif x == a % width and (y == (b + 1) % height or y == (b + 2) % height):
        return 2
    elif x == (a + 1) % width and y == (b + 3) % height:
        return 3
    elif x == (a + 3) % width and y == b % height:
        return 4
    elif x == (a + 4) % width and (y == (b + 1) % height or y == (b + 2) % height):
        return 5
    elif x == (a + 3) % width and y == (b + 3) % height:
        return 6
    elif (a + 1) % pattern_width <= x <= (a + 3) % pattern_width and (b + 1) % pattern_height <= y <= (b + 2) % pattern_height:
        return 7
    elif x == (a + 2) % width and (y == b % height or y == (b + 3) % height):
        return 8
#    elif (a + 1) % pattern_width <= x % pattern_width <= (a + 3) % pattern_width and (b + 1) % pattern_height <= y % pattern_height <= (b + 2) % height:
#        return 7
#    elif x % pattern_width == (a + 2) % width and (y % pattern_height == b % height or y % pattern_height == (b + 3) % height):
#        return 8
    else:
#        return None
#        print x % pattern_width, y % pattern_height, (a + 1) % pattern_width, '<=', x, '<=', (a + 3) % pattern_width, ',', (a + 1) % pattern_height, '<=', y, '<=', (a + 2) % height
        return ' '

#d = np.array([[compartment_factory(x, y) for x in range(width)] for y in range(height)])
#print_distribution(d)
#print
#exit()

d = np.array([[' ' for _ in range(height)] for _ in range(width)])
#print d.shape

w = 4
h = 4

a = 0
b = 0
n = m = 0
#for j in range(h):
#    for i in range(w):
for x in range(pattern_width):
    x = x + a
    for y in range(pattern_height):
        y = y + b
        c = compartment_factory(x, y)
#        print _, a, b, x, y, c
        if c != ' ':#is not None:
            d[x, y] = c
            print c,
    print
print
#        a += 4
#    a = n
#    a += 4
#    n = a
#    b = m
#    b += 5
#    m = b


#for x in range(40):
#    print x % 4
print_distribution(d)

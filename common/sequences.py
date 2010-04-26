def overlapping(left, right):
    for c in reversed(range(len(right))):
        c += 1
        r = right[0:c]
        l = left[-c:]
        if list(l) == list(r):
            return r
    t = type(left) or type(right)
    return t()
        
def join_overlapping(left, right):
    o = overlapping(left, right)
    t = type(o)
    l = list(left[:])
    l += right[len(o):]
    return t(l)
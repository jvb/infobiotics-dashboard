# tests if None is False: it is.
 
readable = None
#readable = True
#readable = False

if not readable:
    print '1'
    
if readable is not None:
    print '2'
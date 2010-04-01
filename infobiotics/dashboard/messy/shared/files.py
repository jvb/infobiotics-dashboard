import os


def whereis(program):
    '''
    from: http://jimmyg.org/blog/2009/working-with-python-subprocess.html
    '''
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None


#def can_open(path, mode='r'):
#    try:
#        file = open(path, mode)
#        file.close()
#        return True
#    except:
#        return False
#
#def can_read(path):
#    return can_open(path, 'r')
#
#def can_write(path):
#    result = can_open(path, 'w')
#    return result

'''
Note: "open(path, 'w')" will overwrite the file specified by path! Uses
"if not access(self.temporal_formulas, W_OK):" instead.
'''

def can_access(path, mode=os.F_OK):
    '''
    
    os.F_OK tests the existence of a path
    
    http://docs.python.org/library/os.html#files-and-directories
    
    '''
    return os.access(path, mode)

def can_read(path):
    return can_access(path, os.R_OK)

def can_write(path):
    if can_access(path):
        return can_access(path, os.W_OK)
    else:
        print os.path.dirname(path)
        return can_write(os.path.dirname(path))

#if __name__ == '__main__':
#    print can_write('~/.bashrc')
#    print can_write('/home/jvb/.bashrc')

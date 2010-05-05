#__all__ = ['can_access', '']

import os, errno
from sequences import join_overlapping

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise



#def path_join_overlapping(left, right):
#    return os.path.join(*join_overlapping(left, right))
def path_join_overlapping(list_of_split_directories):
    return os.path.join(*reduce(join_overlapping, list_of_split_directories))

def split_directories(path, isdir=False):
    ''' Splits paths into a tuple of directory names (including '/'). 
    
    if isdir == True: interpret first basename as a directory. 
    '''
    directories = []
    dirname, basename = os.path.split(path)
    if isdir:
        directories.append(basename)
    while dirname != '':
        dirname, basename = os.path.split(dirname)
        if basename != '':
            directories.append(basename)
        elif dirname == os.path.sep:
            directories.append(dirname)
            break#dirname = ''
    return tuple(reversed(directories))

def can_access(path, mode=os.F_OK):
    '''
    os.F_OK tests the existence of a path
    
    http://docs.python.org/library/os.html#files-and-directories
    '''
    return os.access(path, mode)

def can_execute(path):
    return can_access(path, os.X_OK)

def can_read(path):
    return can_access(path, os.R_OK)

def read(file, mode='r'):
    if not can_read(file):
        raise IOError("Cannot read '%s'." % file)
    else:
        return open(file, mode)

def read_binary(file):
    return read(file, mode='rb')        

def can_write(path):
    ''' When testing whether a file can be written to the statement:
        "open(path, 'w')" alone will overwrite the file specified by path!
        Use "if not can_write(self.temporal_formulas):" instead.
    '''
    if can_access(path):
        return can_access(path, os.W_OK)
    else:
        # if we got here then the file might not exist but we can still test if
        # the directory it should be in is writable.
        return can_write(os.path.dirname(os.path.abspath(path)))

def write(file, mode='w'):
    if not can_write(file):
        raise IOError("Cannot write '%s'." % file)
    else:
        return open(file, mode)

def append(file):
    return write(file, mode='a')

def update(file):
    return write(file, mode='r+')

#def which(program):
#    ''' from: 'http://jimmyg.org/blog/2009/working-with-python-subprocess.html' as whereis '''
#    for path in os.environ.get('PATH', '').split(':'):
#        if os.path.exists(os.path.join(path, program)) and not os.path.isdir(os.path.join(path, program)):
#            return os.path.join(path, program)
#    return None
from thirdparty.which import which
    
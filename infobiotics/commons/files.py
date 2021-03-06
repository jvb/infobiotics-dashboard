#__all__ = ['can_access', '']

import os, errno
from sequences import join_overlapping

def mkdir_p(path):
    # confirmed in http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write/273208#273208
    try:
        os.makedirs(path)
    except OSError, exc: # Python >2.5
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

def can_access_file(path):
    ''' Return whether path is an existing file. '''
    return can_access(path) if os.path.split(path)[1] != '' else False

def can_read_file(path):
    ''' Return whether path is an existing readable file. '''
    return can_access(path, os.R_OK) if can_access_file(path) else False

def can_write_file(path):
    if os.path.isdir(path):
        return False
    return can_write(path) if os.path.split(path)[1] != '' else False

def read(file, mode='r'):
    if not can_read(file):
        raise IOError("Cannot read '%s' (current working directory = '%s')." % (file, os.getcwd()))
    else:
        return open(file, mode)

def read_binary(file):
    return read(file, mode='rb')

def can_write(path=''):
    ''' When testing whether a file or directory can be written to.
        
        "open(path, 'w')" alone will overwrite the file specified by path!
        Use "if not can_write(self.temporal_formulas):" instead.
    '''
    if path.strip() == '':
        raise ValueError("Path empty.")
    if can_access(path):
        return can_access(path, os.W_OK)
    else:
        # if we get here then the file might not exist but we can still test if
        # the directory it should be in is writable.
        return can_write(os.path.dirname(os.path.abspath(path)))

# aliases
accessible = can_access
readable = can_read
writable = can_write
executable = can_execute


def write(file, mode='w'):
    if not can_write(file):
        raise IOError("Cannot write '%s'." % file)
    else:
        return open(file, mode)

def append(file):
    return write(file, mode='a')

def update(file):
    return write(file, mode='r+')


import sys, fileinput
def prepend_line_to_file(line, file_name):
    ''' Insert a line at the beginning of a file. 
    
    Lifted from: http://python-forum.com/pythonforum/viewtopic.php?f=3&t=9793#p44799
    
    '''
    fobj = fileinput.FileInput(file_name, inplace=1)
    first_line = fobj.readline()
    sys.stdout.write("%s\n%s" % (line, first_line))
    for line in fobj:
        sys.stdout.write("%s" % line)
    fobj.close()


if __name__ == '__main__':
    print accessible('/tmp/made_up_name')
    print writable('/tmp/made_up_dir/made_up_name')
    
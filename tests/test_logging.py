from infobiotics.shared.api import can_read, can_write

import logging
test_logger = logging.getLogger('test')

import sys
test_logger.addHandler(logging.StreamHandler(sys.stderr))

# programmatically set log level to DEBUG
test_logger.setLevel(logging.DEBUG)

# imitate user choosing to ignore log messages up to and including WARNING (setting log level to ERROR)
#logging.disable(logging.WARN)

file = 'test'
test_logger.debug("Trying to read file '%s'", file) # ignored
try:
    
    if can_read(file):
        f = open(file, 'r')
    else:
        raise IOError("Failed to read file '%s'" % file)

    if can_write(file):
        f = open(file, 'w')
    else:
        raise IOError("Failed to write file '%s'" % file)
    
except IOError, e:
#    test_logger.error(e)
    test_logger.exception(e)
    sys.exit(1)

print 'Success'
sys.exit(0)
    
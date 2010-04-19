from infobiotics.shared.api import can_read, can_write, read, write

import logging
#logging.debug('testing root logger')
test_logger = logging.getLogger('test')

import sys
test_handler = logging.StreamHandler(sys.stderr)#stdout))
#test_handler.format()
test_logger.addHandler(test_handler)

# programmatically set log level to DEBUG
test_logger.setLevel(logging.DEBUG)

# imitate user choosing to ignore log messages up to and including WARNING (setting log level to ERROR)
#logging.disable(logging.WARN)

file = 'test'
test_logger.debug("Trying to read file '%s'", file) # ignored by logging.disable(logging.WARN)
try:
    
#    if can_read(file):
#        f = open(file, 'r')
#    else:
#        raise IOError("Failed to read file '%s'" % file)
    f = write(file)
    test_logger.debug(f)
    f.write('Success\n')
    f.close()
    test_logger.debug(f)

#    if can_write(file):
#        f = open(file, 'w')
#    else:
#        raise IOError("Failed to write file '%s'" % file)
    f = read(file)
    test_logger.debug(f)
    lines = f.readlines()
    test_logger.debug("'%s' has %d lines", file, len(lines))
    for line in lines:
        print line
    f.close()
    test_logger.debug(f)
    
except IOError, e:
#    test_logger.exception(e) # includes traceback
#    test_logger.error(e)
    test_logger.error("Failed to read file '%s'" % file) # overrides message
    sys.exit(1)

sys.exit(0)
    
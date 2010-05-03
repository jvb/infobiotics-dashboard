''' print 1:100 to stdout and 10:100:10 to stderr but fail at 50 '''  
import sys
import time
for i in range(0,100):
    if i > 1 and i % 50 == 0:
        sys.exit(1)
    if i > 1 and i % 10 == 0:
        sys.stderr.write('%s\n' % i)
    sys.stdout.write('%s\n' % i)
    time.sleep(0.1)
#    sys.stdout.flush()
sys.exit(0)
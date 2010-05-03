#!/usr/bin/env python

import time
import sys

for i in range(0,10):
#    print i
    sys.stdout.write('%s\n'%i)
    time.sleep(0.1)
    sys.stdout.flush()

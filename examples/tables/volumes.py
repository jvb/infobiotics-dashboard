#!/usr/bin/env python

import sys
import tables
f = tables.openFile(sys.argv[1])
print f.root.run1.volumes

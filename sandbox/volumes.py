#!/usr/bin/env python
import sys
import tables
root = tables.openFile(sys.argv[1]).root
print root.run1.volumes

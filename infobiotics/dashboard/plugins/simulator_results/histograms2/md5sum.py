#!/usr/bin/python
# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


import hashlib


def md5sum(fileName, blockSize=2**20):
    file = open(fileName, 'r')
    md5 = hashlib.md5()
    while True:
        data = file.read(blockSize)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()



if __name__ == '__main__':
    import sys
    print sys.argv
    print md5sum(sys.argv[1])
    
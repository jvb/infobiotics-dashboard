#!/usr/bin/python
# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: md5sum.py 366 2010-01-13 20:16:01Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/shared/md5sum.py $
# $Author: jvb $
# $Revision: 366 $
# $Date: 2010-01-13 20:16:01 +0000 (Wed, 13 Jan 2010) $


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
    
#!/bin/bash

for file in `find infobiotics -type f | egrep -v '(\/\.svn\/)|(\.pyc)|(\.ui)'`
do
	echo "    '$file',"
done
# > files 

python make-deb.py

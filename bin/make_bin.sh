#!/bin/bash
set -o nounset
set -o errexit

names="infobiotics-dashboard
infobiotics-workbench
ibw"

exts=".py
.pyw"

for name in $names
do
    for ext in $exts ""
    do
    	f=$name$ext
    	cp _ibw.py $f && chmod +x $f
    done
done

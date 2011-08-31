#!/bin/bash
./clean.sh
python setup.py sdist
cd dist
t=`ls InfobioticsDashboard-*.tar.gz`
d="${t%.tar.gz}"
tar -xzvf $t
cd $d
export PYTHONPATH=`pwd`
#echo $PYTHONPATH 
python -c 'import infobiotics.dashboard.run as run; run.main()'

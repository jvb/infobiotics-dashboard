#!/bin/bash
./clean.sh
cd bin
./make_bin.sh
cd ..
python setup.py sdist
cd dist
t=`ls InfobioticsDashboard-*.tar.gz`
d="${t%.tar.gz}"
tar -xzvf $t
cd $d
export PYTHONPATH=`pwd`
#python -c 'import infobiotics.dashboard.run as run; run.main()'
echo
echo "If not source ./sdist.sh do"
echo "export PYTHONPATH=$PYTHONPATH; echo \$PYTHONPATH; cd $PYTHONPATH" 


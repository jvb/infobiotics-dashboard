#!/bin/bash

version=0.0.13
name=InfobioticsDashboard-$version
virtualenvname=$name--no-site-packages
home=`pwd`

./clean.sh
source /home/jvb/.venvburrito/startup.sh
rmvirtualenv $virtualenvname
python setup.py sdist
cd dist
tar -xzvf $name.tar.gz
cd $name
mkvirtualenv --distribute --no-site-packages $virtualenvname
easy_install -U distribute
easy_install numpy
cdsitepackages
pymodules=/usr/lib/pymodules/python2.7
ln -s $pymodules/sip.so
ln -s $pymodules/sipconfig.py
ln -s $pymodules/PyQt4
ln -s $pymodules/matplotlib
ln -s $pymodules/dateutil
ln -s $pymodules/vtk
ln -s $pymodules/xlwt
ln -s $pymodules/docutils
ln -s $pymodules/numpy
dist_packages=/usr/lib/python2.7/dist-packages
ln -s $dist_packages/pygments
ln -s $dist_packages/configobj.py
ln -s $dist_packages/tables
ln -s $dist_packages/pytz
#pip install pygments docutils ConfigObj
#pip install numpy
#pip install http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.0/matplotlib-1.0.0.tar.gz?use_mirror=sunet&ts=1279878271
#pip install numexpr
#pip install cython
#pip install tables
#cd ../../../build/tables/tables/
#cython utilsExtension.pyx
python setup.py install

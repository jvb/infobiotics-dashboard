#!/bin/bash
mkvirtualenv -p python2.6 --no-site-packages --distribute ETS_trunk && cdsitepackages
ln -s /usr/lib/pymodules/python2.6/vtk
ln -s /usr/lib/pyshared/python2.6/PyQt4
ln -s /usr/lib/pyshared/python2.6/sip.so
#ln -s /usr/lib/pymodules/python2.6/sipconfig.py
pip install numpy
pip install http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.0/matplotlib-1.0.0.tar.gz?use_mirror=sunet&ts=1279878271
pip install numexpr
pip install cython
pip install tables
cd ../../../build/tables/tables/
cython utilsExtension.pyx
cd ..
python setup.py install
cdsitepackages
pip freeze

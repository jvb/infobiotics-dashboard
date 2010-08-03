#!/bin/bash
# creates a minimal Python installation, borrowing only PyQt4 and VTK.
mkvirtualenv -p python2.6 --distribute --no-site-packages infobiotics-dashboard && cdsitepackages && ln -s /usr/lib/pymodules/python2.6/vtk && ln -s /usr/lib/python2.6/dist-packages/PyQt4 && ln -s /usr/lib/python2.6/dist-packages/sip.so && ln -s /usr/lib/python2.6/dist-packages/sipconfig.py && easy_install pip && pip install numpy && pip install http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-0.99.1/matplotlib-0.99.1.2.tar.gz/download && pip freeze


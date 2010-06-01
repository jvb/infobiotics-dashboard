#!/bin/bash
bash clean.sh
export ETS_TOOLKIT=qt4
python setup.py py2exe
mkdir -p dist/enthought/tvtk/tvtk_classes
unzip -q -d dist/enthought/tvtk/tvtk_classes /cygdrive/c/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip
#rm -rf build
dist/infobiotics-dashboard.exe
cat dist/infobiotics-dashboard.exe.log
cat dist/pexpect_error.txt

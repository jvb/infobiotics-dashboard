#!/bin/bash
export ETS_TOOLKIT=qt4
rm -rf dist
Python setup.py py2exe &&
unzip -q -d dist/enthought/tvtk/tvtk_classes /cygdrive/c/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip &&

#cp /cygdrive/c/Python26/Scripts/pywintypes26.dll dist/

dist/infobiotics-dashboard.exe
cat dist/infobiotics-dashboard.exe.log
cat dist/pexpect_error.txt
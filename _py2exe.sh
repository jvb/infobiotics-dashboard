#!/bin/bash
export ETS_TOOLKIT=qt4
#PYTHON=/Library/Frameworks/Python.framework/Versions/Current/bin/python
rm -rf dist
#build
Python setup.py py2exe
#cd dist
#unzip -q -d library library.zip
#rm library.zip
#cp /cygdrive/c/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip library/enthought/tvtk
#cd library/enthought/tvtk
#unzip -q -d tvtk_classes tvtk_classes.zip
unzip -q -d dist/enthought/tvtk/tvtk_classes /cygdrive/c/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip 
#rm tvtk_classes.zip
#cd ../..
#zip -q -0 -r ../library.zip *
#cd ..
#rm -r library

#cp /cygdrive/c/Python26/Scripts/pywintypes26.dll dist/

dist/infobiotics-dashboard.exe
cat dist/infobiotics-dashboard.exe.log
cat dist/pexpect_error.txt
#!/bin/bash
chmod +x bin/infobiotics-dashboard.py
rm -rf build dist
python setup.py py2app
touch dist/InfobioticsDashboard.app/Contents/Resources/qt.conf 
cp /Library/Frameworks/Python.framework/Versions/6.1/lib/libhdf5.6.dylib dist/InfobioticsDashboard.app/Contents/MacOS/../Frameworks/libhdf5.6.dylib
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip
#CWD=$PWD
#cd dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6
#zip -0 -r site-packages.zip site-packages | grep ui/qt4
#cd $CWD
#rm -rf dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/
echo dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard

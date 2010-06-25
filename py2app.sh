#!/bin/bash
export ETS_TOOLKIT=qt4
PYTHON=/Library/Frameworks/Python.framework/Versions/Current/bin/python
chmod +x bin/infobiotics-dashboard.py
rm -rf build dist
${PYTHON} setup.py py2app &&
touch dist/InfobioticsDashboard.app/Contents/Resources/qt.conf &&
cp /Library/Frameworks/Python.framework/Versions/6.1/lib/libhdf5.6.dylib dist/InfobioticsDashboard.app/Contents/MacOS/../Frameworks/libhdf5.6.dylib &&
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages &&
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip &&
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes &&
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip
echo 
echo "To run use:"
echo "dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard"
dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard


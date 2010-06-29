#!/bin/bash

echo "freezing with py2app"
echo "additional flags (see 'python setup.py py2app --help') will by parsed to py2app"
echo

export ETS_TOOLKIT=qt4

PYTHON=/Library/Frameworks/Python.framework/Versions/Current/bin/python

# cleaning
#rm -rf build dist
bash ./clean.sh


# pre-freeze
chmod +x bin/infobiotics-dashboard.py


# freeze
easy_install pip
pip install py2app pexpect

${PYTHON} setup.py py2app $* &&
#--no-strip


# post-freeze

echo "creating qt.conf" &&
touch dist/InfobioticsDashboard.app/Contents/Resources/qt.conf &&

echo "unzipping tvtk_classes.zip in site-packages.zip" &&
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages &&
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip &&
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes &&
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip &&

echo "copying libhdf5.6.dylib (could do this using 'py2app --frameworks'?)" &&
cp /Library/Frameworks/Python.framework/Versions/Current/lib/libhdf5.6.dylib dist/InfobioticsDashboard.app/Contents/MacOS/../Frameworks/libhdf5.6.dylib &&

# Tiger-specific
#install_name_tool -change "@rpath/libfreetype.6.dylib" "@loader_path/../../../../Frameworks/libfreetype.6.dylib" dist/Infobiotics\ Dashboard.app/Contents/Resources/lib/python2.6/matplotlib/ft2font.so


# testing

echo &&
echo "To run use:" &&
echo "dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard" &&
echo &&
echo "Running now" &&
dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard

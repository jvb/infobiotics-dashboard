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


# copy missing libraries
cp /Library/Frameworks/Python.framework/Versions/6.2/lib/libmkl_*.dylib /Library/Frameworks/Python.framework/Versions/6.2/lib/libiomp5.dylib /Library/Frameworks/Python.framework/Versions/6.2/lib/libpng12.0.dylib  dist/InfobioticsDashboard.app/Contents/Frameworks/

# fix path
install_name_tool -change @rpath/libmkl_lapack.dylib @executable_path/../Frameworks/libmkl_lapack.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/numpy/linalg/lapack_lite.so
install_name_tool -change @rpath/libmkl_intel.dylib @executable_path/../Frameworks/libmkl_intel.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/numpy/linalg/lapack_lite.so
install_name_tool -change @rpath/libmkl_intel_thread.dylib @executable_path/../Frameworks/libmkl_intel_thread.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/numpy/linalg/lapack_lite.so
install_name_tool -change @rpath/libmkl_core.dylib @executable_path/../Frameworks/libmkl_core.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/numpy/linalg/lapack_lite.so
install_name_tool -change @rpath/libmkl_p4m.dylib @executable_path/../Frameworks/libmkl_p4m.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/numpy/linalg/lapack_lite.so
install_name_tool -change @rpath/libmkl_p4p.dylib @executable_path/../Frameworks/libmkl_p4p.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/numpy/linalg/lapack_lite.so

install_name_tool -change  @rpath/libfreetype.6.dylib /usr/X11/lib/libfreetype.6.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/matplotlib/backends/_backend_agg.so
install_name_tool -change  @rpath/libfreetype.6.dylib /usr/X11/lib/libfreetype.6.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/matplotlib/ft2font.so 
install_name_tool -change  @rpath/libpng12.0.dylib @executable_path/../Frameworks/libpng12.0.dylib dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/matplotlib/_png.so

# testing

echo "all built ok"

#echo &&
#echo "To run use:" &&
#echo "dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard" &&
#echo &&
#echo "Running now" &&
#dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard

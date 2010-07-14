#!/bin/bash
export http_proxy=http://wwwcache-20.cs.nott.ac.uk:3128
export https_proxy=https://wwwcache-20.cs.nott.ac.uk:3128
bash clean.sh
export ETS_TOOLKIT=qt4
python setup.py py2exe
for i in $(cat windows_xp_missing_dlls.txt | cut -f 3 -d ' ' | sed 's/\.dll.* $/\.dll/g' | sed 's/\.DLL.*$/\.DLL/g') ; do cp $i dist/ ; done
mkdir -p dist/enthought/tvtk/tvtk_classes
current_drive=`python -c 'import os, sys; sys.stdout.write(os.getcwd()[0].lower())'`
cp -r /cygdrive/$current_drive/Python26/Scripts/*.dll dist/
ls dist/*.dll
unzip -q -d dist/enthought/tvtk/tvtk_classes /cygdrive/$current_drive/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip
#rm -rf build
#dist/infobiotics-dashboard.exe
#cat dist/infobiotics-dashboard.exe.log
#cat dist/pexpect_error.txt

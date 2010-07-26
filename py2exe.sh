#!/bin/bash

export http_proxy=http://wwwcache-20.cs.nott.ac.uk:3128
export https_proxy=https://wwwcache-20.cs.nott.ac.uk:3128

export ETS_TOOLKIT=qt4

bash clean.sh

python setup.py py2exe

current_drive=`python -c 'import os, sys; sys.stdout.write(os.getcwd()[0].lower())'`

mkdir -p dist/enthought/tvtk/tvtk_classes
unzip -q -d dist/enthought/tvtk/tvtk_classes /cygdrive/$current_drive/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip

#TODO mv windows_xp_missing_dlls.txt HERE
for i in $(cat windows_xp_missing_dlls.txt | cut -f 3 -d ' ' | sed 's/\.dll.* $/\.dll/g' | sed 's/\.DLL.*$/\.DLL/g' | sed 's/D:/C:/g') ; do cp $i dist/ ; done

cp -r /cygdrive/$current_drive/Python26/Scripts/*.dll dist/
#ls dist/*.dll

#rm -rf build

#dist/infobiotics-dashboard.exe
#cat dist/infobiotics-dashboard.exe.log
#cat dist/pexpect_error.txt

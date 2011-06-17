#!/bin/bash

#export http_proxy=http://wwwcache-20.cs.nott.ac.uk:3128
#export https_proxy=https://wwwcache-20.cs.nott.ac.uk:3128

export ETS_TOOLKIT=qt4

bash clean.sh

# fix build_exe deprecated sets (only needs to happen once)
py2exe_dir=`python -c "import py2exe, sys, os.path; sys.stdout.write(os.path.dirname(py2exe.__file__))"`
cp -f py2exe/build_exe.py $py2exe_dir
cp -f py2exe/boot_common.py $py2exe_dir

python setup.py py2exe

current_drive=`python -c 'import os, sys; sys.stdout.write(os.getcwd()[0].lower())'`

mkdir -p dist/enthought/tvtk/tvtk_classes
unzip -q -d dist/enthought/tvtk/tvtk_classes /cygdrive/$current_drive/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip

for i in $(cat py2exe/windows_xp_missing_dlls.txt | cut -f 3 -d ' ' | sed 's/\.dll.* $/\.dll/g' | sed 's/\.DLL.*$/\.DLL/g' | sed "s/D:/$current_drive:/g") ; do cp $i dist/ ; done

cp -r /cygdrive/$current_drive/Python26/Scripts/*.dll dist/

#dist/infobiotics-dashboard.exe
#cat dist/infobiotics-dashboard.exe.log

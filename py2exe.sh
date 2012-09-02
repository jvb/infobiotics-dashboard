#!/bin/sh

# 


echo "freezing with py2exe (run under cygwin)"
#TODO echo "additional flags (see 'python setup.py py2exe --help') will by parsed to py2exe"
echo


# cleaning

# remove PKG_INFO, setup.cfg, .pyc and .class files; build, debian, dist and tmp directories; Debian packages; distribute and InfobioticsDashboard eggs  
bash .clean.sh


# pre-freezing

# make files executable
#TODO chmod +x bin/*

# set environment variables
export ETS_TOOLKIT=qt4

# fix build_exe deprecated sets (only needs to happen once)
py2exe_dir=`python -c "import py2exe, sys, os.path; sys.stdout.write(os.path.dirname(py2exe.__file__))"`
cp -f py2exe/build_exe.py $py2exe_dir
cp -f py2exe/boot_common.py $py2exe_dir


# freezing

# run py2exe
#${PYTHON} setup.py py2app $* &&
##--no-strip
python setup.py py2exe


# post-freezing

# determine current drive (letter)
current_drive=`python -c 'import os, sys; sys.stdout.write(os.getcwd()[0].lower())'`

# add TVTK classes zip file to library; fixes: 'ImportError: TVTK not built properly. Unable to find either a directory: /home/jvb/git/infobiotics-dashboard/dist/library.zip/tvtk/tvtk_classes or a file: /home/jvb/git/infobiotics-dashboard/dist/library.zip/tvtk/tvtk_classes.zip with the TVTK classes.'
#mkdir -p dist/enthought/tvtk/tvtk_classes
mkdir -p dist/tvtk/tvtk_classes
#unzip -q -d dist/enthought/tvtk/tvtk_classes /cygdrive/$current_drive/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip
unzip -q -d dist/tvtk/tvtk_classes /cygdrive/$current_drive/Python26/Lib/site-packages/enthought/tvtk/tvtk_classes.zip

# add missing dll files under Windows XP 
for i in $(cat py2exe/windows_xp_missing_dlls.txt | cut -f 3 -d ' ' | sed 's/\.dll.* $/\.dll/g' | sed 's/\.DLL.*$/\.DLL/g' | sed "s/D:/$current_drive:/g") ; do cp $i dist/ ; done

# add other dll files from Python
cp -r /cygdrive/$current_drive/Python26/Scripts/*.dll dist/


# testing

# run infobiotics-dashboard
#dist/infobiotics-dashboard.exe

# print log
#cat dist/infobiotics-dashboard.exe.log

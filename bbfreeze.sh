#!/bin/sh

# 


echo "freezing with bbfreeze"
#TODO echo "additional flags (see 'python setup.py py2app --help') will by parsed to py2app"
echo


# cleaning

# remove PKG_INFO, setup.cfg, .pyc and .class files; build, debian, dist and tmp directories; Debian packages; distribute and InfobioticsDashboard eggs  
bash .clean.sh


# pre-freezing

# make files executable
#TODO chmod +x bin/*

# set environment variables
export ETS_TOOLKIT=qt4

# install bbreeze (using pip)
##TODO easy_install pip
#TODO apt-get install python-pip 
#TODO pip install bbfreeze


# freezing

# run bbreeze
#${PYTHON} setup.py py2app $* &&
##--no-strip
python freeze.py


# post-freezing

# add TVTK classes zip file to library; fixes: 'ImportError: TVTK not built properly. Unable to find either a directory: /home/jvb/git/infobiotics-dashboard/dist/library.zip/tvtk/tvtk_classes or a file: /home/jvb/git/infobiotics-dashboard/dist/library.zip/tvtk/tvtk_classes.zip with the TVTK classes.'
# --------------------------
# 1
#echo "unzipping tvtk_classes.zip in site-packages.zip" &&
#unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages &&
#rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip &&
#unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes &&
#rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip &&

# 2
##mkdir -p dist/tvtk/tvtk_classes
##unzip -q -d dist/tvtk/tvtk_classes /usr/share/pyshared/tvtk/tvtk_classes.zip
#mkdir tvtk
#cp /usr/share/pyshared/tvtk/tvtk_classes.zip tvtk/
#zip tvtk/ dist/library.zip

# history
echo <<HERE
mv library.zip _library.zip
unzip _library.zip -d library.zip
cd library.zip/tvtk/
ls
cd ..
cd ..
rm library.zip
mv _library.zip library.zip
unzip library.zip -d _library
unzip _library/tvtk/tvtk_classes.zip 
rm -r tvtk_classes/
unzip _library/tvtk/tvtk_classes.zip -d _library/tvtk/
cd library
cd _library
zip ../library.zip *
zip -u ../library.zip *
ls .. | grep libr


locate tvtk_classes.zip
ll /usr/lib/python2.7/dist-packages/tvtk/tvtk_classes.zip
/usr/share/pyshared/tvtk/tvtk_classes.zip
ll /usr/share/pyshared/tvtk/tvtk_classes.zip
less py2exe.sh 
locate tvtk_classes.zip
unzip -q -d dist/tvtk/tvtk_classes /usr/lib/pyshared/tvtk/tvtk_classes.zip
unzip -q -d dist/tvtk/tvtk_classes /usr/share/pyshared/tvtk/tvtk_classes.zip
dist/infobiotics-dashboard 
--h
ll dist/library.zip 
mkdir dist/library.zip
zip --help
zip -g dist/library.zip /usr/share/pyshared/tvtk/tvtk_classes.zip
sudo apt-get install zip
zip -g dist/library.zip /usr/share/pyshared/tvtk/tvtk_classes.zip
dist/infobiotics-dashboard 
zip --help
HERE
# --------------------------


# testing

# run infobiotics-dashboard
dist/infobiotics-dashboard

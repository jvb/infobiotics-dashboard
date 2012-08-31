#!/bin/bash

# use CS proxy
export http_proxy=http://wwwcache-20.cs.nott.ac.uk:3128

# variables: 

# TMPDIR is a prefix: the directory 'PyQt4_Qsci' is created inside it
TMPDIR=/var/tmp

# EPDVER and PYVER change with the version of EPD, update as necessary
EPDVER=6.2
PYVER=2.6

echo "Installer for sip/PyQt4/QScintilla"
echo
echo "Please ensure that the following dependencies have been installed before continuing:"
echo "32-bit Cocoa-based Qt (http://get.qt.nokia.com/qt/source/qt-mac-cocoa-opensource-4.6.2.dmg)"
echo "Enthought Python Distribution (http://www.enthought.com/products/edudownload.php)"
echo
echo "Run this script in a new terminal *after* EPD has been installed, otherwise it will use the system Python and fail."
echo
echo "Press ENTER to continue or Ctrl-C to abort."
read
echo
sudo echo "Started..."

# fix symbolic links in EPD
#sudo rm -rf /Library/Frameworks/Python.framework/Versions/$EPDVER/include/python$EPDVER
#sudo rm -rf /Library/Frameworks/Python.framework/Versions/$EPDVER/lib/python$EPDVER
sudo ln -s /Library/Frameworks/Python.framework/Versions/$EPDVER/include/python$PYVER /Library/Frameworks/Python.framework/Versions/$EPDVER/include/python$EPDVER
sudo ln -s /Library/Frameworks/Python.framework/Versions/$EPDVER/lib/python$PYVER /Library/Frameworks/Python.framework/Versions/$EPDVER/lib/python$EPDVER

# change to temporary directory
mkdir -p $TMPDIR/PyQt4_Qsci && cd $TMPDIR/PyQt4_Qsci

# sip
SIP_VERSION=4.10.2
if [ ! -f sip-$SIP_VERSION.tar.gz ]
then
    ftp http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-$SIP_VERSION.tar.gz
fi
tar -xzf sip-$SIP_VERSION.tar.gz && cd sip-$SIP_VERSION && python configure.py --arch=i386 && make && sudo make install && cd ..

# qscintilla2
QSCI_VERSION=2.4.3
if [ ! -f QScintilla-gpl-$QSCI_VERSION.tar.gz ]
then
    ftp http://www.riverbankcomputing.co.uk/static/Downloads/QScintilla2/QScintilla-gpl-$QSCI_VERSION.tar.gz
fi
tar -xzf  QScintilla-gpl-$QSCI_VERSION.tar.gz && cd QScintilla-gpl-$QSCI_VERSION/Qt4 && qmake -spec macx-g++ qscintilla.pro
# backup Makefile
cp Makefile _Makefile 
# fix Makefile according to: http://markmail.org/thread/opnfqsq7e5zbsjpf
sed -e 's/= g++/= g++ -arch i386/' Makefile > Makefile_ && cp Makefile_ Makefile
#make clean && 
make && sudo make install && cd ../..

# PyQt
PYQT_VERSION=4.7.3
if [ ! -f PyQt-mac-gpl-$PYQT_VERSION.tar.gz ]
then
    ftp http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-mac-gpl-$PYQT_VERSION.tar.gz
fi
tar -xzf PyQt-mac-gpl-$PYQT_VERSION.tar.gz && cd PyQt-mac-gpl-$PYQT_VERSION && python configure.py --use-arch=i386 <<HERE
yes
HERE
make && sudo make install && cd ..

# qscintilla2 Python module: qsci
cd QScintilla-gpl-$QSCI_VERSION/Python && python configure.py && make && sudo make install && cd ..

# test
python -c 'import PyQt4; print PyQt4'

python <<HERE
from enthought.traits.api import HasTraits, Code

class Test(HasTraits): 
    code = Code

Test().configure_traits()
HERE

#!/bin/bash

echo "Installer for sip/PyQt4/QScintilla with 32-bit Cocoa-based Qt and 32-bit EPD Python interpreter"
echo
echo "Please ensure that the following dependencies have been installed before continuing:"
echo "32-bit Cocoa-based Qt (http://get.qt.nokia.com/qt/source/qt-mac-cocoa-opensource-4.6.2.dmg)"
echo " an academic version of Enthought Python Distribution 6.1 (http://www.enthought.com/products/edudownload.php)"
echo
echo "Press ENTER to continue or Ctrl-C to abort."
read
echo
sudo echo "Started..."

# change to temporary directory
TMPDIR=/tmp
mkdir -p $TMPDIR/PyQt4 && cd $TMPDIR/PyQt4

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
make clean && make && sudo make install && cd ..

# PyQt
PYQT_VERSION=4.7.3
if [ ! -f PyQt-mac-gpl-$PYQT_VERSION.tar.gz ]
then
    ftp http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-mac-gpl-$PYQT_VERSION.tar.gz
fi
tar -xzf PyQt-mac-gpl-$PYQT_VERSION.tar.gz && cd PyQt-mac-gpl-$PYQT_VERSION && python configure.py --use-arch=i386 && make && sudo make install && cd ..

# qscintilla2 Python module: qsci
cd QScintilla-gpl-$QSCI_VERSION/Python && python configure.py && make && sudo make install && cd ..

# test
python -c 'import PyQt4; print PyQt4'


#!/bin/sh

PKGNAME=$(cat NAME.txt)
PKGVER=$(cat VERSION.txt)
PKGFULL=$PKGNAME-$PKGVER
MAINTAINER="Jonathan Blakes <jvb@cs.nott.ac.uk>"
PYPKGNAME=${PKGNAME}
PYDEPS="python-vtk, python-qt4, python-qscintilla2, python-numpy (>= 1.4.1), python-matplotlib, python-pexpect, mcss, poptimizer, pmodelchecker, python-apptools (>=3.3.2), python-traitsbackendqt (=3.4.0-1), python-traits (=3.4.0-2) | python-traits (=3.4.0-2build1), python-traitsgui (=3.4.0-1), python-enthoughtbase (>=3.0.6), python-envisagecore(>=3.1.2), python-envisageplugins(>=3.1.2), python-tables(>=2.1.2), mayavi2, python-configobj, python-xlwt, python-qt4-gl, python-progressbar, python-setproctitle, python-quantities(>=0.9.0), python-scipy"

echo "creating ${PKGFULL} debian packages..."

echo "creating debian package..."
CWD=$(pwd)
TMPDIR=/tmp/$PKGFULL
TMPFILE=${TMPDIR}/${PKGFULL}.tmp
LOGFILE=${TMPDIR}/${PKGFULL}.log
ARCH="all"

# debian control files
rm -rf ${TMPDIR}
mkdir -p ${TMPDIR}
rm -rf debian
mkdir debian
# changelog
cat << EOF > debian/changelog &&
$PYPKGNAME ($PKGVER) unstable; urgency=low
  * comment here.

 -- $MAINTAINER  $(date '+%a, %d %b %Y %T %z')
EOF
# compat
echo $(dpkg -p debhelper | egrep '^Version:' | cut -f 2 -d ' ' | cut -f 1 -d '.') > debian/compat &&
# control
cat << EOF > debian/control &&
Source: ${PYPKGNAME}
Priority: optional
Maintainer: ${MAINTAINER}
Build-Depends: debhelper (>=7.0.0), python-support (>= 0.6), cdbs (>= 0.4.49)
Standards-Version: 3.8.3.0

Package: ${PYPKGNAME}
Architecture: ${ARCH}
Depends: \${misc:Depends}, \${python:Depends}, ${PYDEPS}
Section: science
Description: Graphical user interface for Infobiotics experiments.
 This package contains the Infobiotics Dashboard, a graphical user interface for 
 the Infobiotics Workbench.
EOF
# copyright
cp COPYING.txt debian/copyright &&
# rules
cat << EOF > debian/rules &&
#!/usr/bin/make -f
# -*- makefile -*-

DEB_PYTHON_SYSTEM := pysupport

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/class/python-distutils.mk
include /usr/share/cdbs/1/rules/simple-patchsys.mk
EOF
chmod a+x debian/rules &&
# pyversion
echo "2.5-" > debian/pyversions &&

# make package
python setup.py -q sdist  &> ${LOGFILE} &&
dpkg-buildpackage -uc -us -rfakeroot > ${LOGFILE}
if [ $? != 0 ]
then
	echo "error: couldn't create python binary package"
	exit 1
fi

mv ../${PKGNAME}_${PKGVER}_all.deb ./ &&
mv ../${PKGNAME}_${PKGVER}.dsc ./ &&
mv ../${PKGNAME}_${PKGVER}.tar.gz ./ &&
rm -f ../${PKGNAME}_${PKGVER}_*.changes

echo "*******************************"
cd $CWD &&
rm -rf $TMPDIR
if [ $? != 0 ]
then
	echo "error: couldn't create python meta package"
	exit 1
fi

# all done
echo "all ${PKGFULL} packages built ok"

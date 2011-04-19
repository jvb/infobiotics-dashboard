#!/bin/sh

PKGBASE=$(cat NAME.txt)
VERSION=$(cat VERSION.txt)
PKGNAME=$PKGBASE-$VERSION
MAINTAINER="Jonathan Blakes <jvb@cs.nott.ac.uk>"
PYPKGNAME=${PKGNAME}
PYPKGBASE=${PKGBASE}
PYDEPS="python-vtk, python-qt4, python-qscintilla2, python-numpy (>= 1.3.0), python-matplotlib, python-pexpect, mcss, poptimizer, pmodelchecker, python-apptools (>=3.3.1), python-traitsbackendqt (>=3.3.0), python-traits (>=3.3.0), python-traitsgui (>=3.3.0), python-enthoughtbase(>=3.0.4), python-envisagecore(>=3.1.2), python-envisageplugins(>=3.1.2), python-tables(>=2.1.2), mayavi2, python-configobj, python-xlwt, python-qt4-gl, python-progressbar, python-setproctitle"
LASTVERSION=$(echo $VERSION | cut -f 3 -d '.')
LASTVERSION=$(echo "${LASTVERSION}-1" | bc)
LASTVERSION="$(echo $VERSION | cut -f1,2 -d '.').${LASTVERSION}"

echo "creating ${PKGBASE} debian packages..."

echo "creating debian package..."
CWD=$(pwd)
TMPDIR=/tmp/$PKGNAME
TMPFILE=${TMPDIR}/${PKGNAME}.tmp
LOGFILE=${TMPDIR}/${PKGNAME}.log
ARCH="all"

# debian control files
rm -rf ${TMPDIR}
mkdir -p ${TMPDIR}
rm -rf debian
mkdir debian
# changelog
cat << EOF > debian/changelog &&
$PYPKGNAME ($VERSION) unstable; urgency=low
  * comment here.

 -- $MAINTAINER  $(date '+%a, %d %b %Y %T %z')
EOF
# compat
echo $(dpkg -p debhelper | egrep '^Version:' | cut -f 2 -d ' ' | cut -f 1 -d '.') > debian/compat &&
# control
cat << EOF > debian/control &&
Source: ${PYPKGNAME}
Section: science
Priority: optional
Maintainer: ${MAINTAINER}
Build-Depends: debhelper (>=7.0.0), python-support (>= 0.6), cdbs (>= 0.4.49)
Standards-Version: 3.8.3.0

Package: ${PYPKGNAME}
Architecture: ${ARCH}
Depends: \${misc:Depends}, \${python:Depends}, ${PKGNAME}, ${PYDEPS}
Replaces: ${PYPKGBASE}-${LASTVERSION}
Description: ${PKGNAME}.
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

mv ../${PKGNAME}_${VERSION}_all.deb ./ &&
mv ../${PKGNAME}_${VERSION}.dsc ./ &&
mv ../${PKGNAME}_${VERSION}.tar.gz ./ &&
rm -f ../${PKGNAME}_${VERSION}_*.changes

# make meta package
echo "making python meta package..."
# create control file
mkdir -p $TMPDIR/$PYPKGBASE/DEBIAN &&
cat << EOF > $TMPDIR/$PYPKGBASE/DEBIAN/control &&
Package: $PYPKGBASE
Version: $VERSION
Section: science
Priority: optional
Architecture: all
Depends: $PYPKGNAME
Replaces: $PYPKGBASE (<< $VERSION)
Maintainer: $MAINTAINER
Description: $PKGNAME
EOF

# make meta package
cd $TMPDIR &&
dpkg-deb --build $PYPKGBASE > ${LOGFILE} &&
mv ${TMPDIR}/$PYPKGBASE.deb $CWD/${PYPKGBASE}_${VERSION}_all.deb &&
cd $CWD &&
rm -rf $TMPDIR
if [ $? != 0 ]
then
	echo "error: couldn't create python meta package"
	exit 1
fi

# all done
echo "all ${PKGBASE} packages built ok"

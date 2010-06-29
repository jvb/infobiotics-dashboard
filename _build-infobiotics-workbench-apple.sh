#!/bin/sh

if [ $# != 1 ]
then
        echo "usage: build-infobiotics-workbench.sh MANIFEST"
        exit 1
fi

MANIFEST=$1
VERSION=$(cat ${MANIFEST} | egrep '^infobiotics-workbench' | cut -f 2 -d ' ')
BUILDDIR=${PWD}
BUILDTMP=${BUILDDIR}/build-tmp
SOFTREPOSRC=/var/root/infobiotics/src
PKGBASE=infobiotics-workbench
PKGNAME=${PKGBASE}
PKGDIR=${BUILDDIR}/${PKGBASE}
TMPFILE=${BUILDIR}/${PKGBASE}.tmp

ARCH=i686-apple-darwin8
ARCHROOT=/usr/local
ARCHBIN=${ARCHROOT}/bin
ARCHLIB=${ARCHROOT}/lib

PKGCONFDIR=/var/root/infobiotics/package-config
FILELIST=${PKGCONFDIR}/filelist-apple
SOFTREPOTMP=/var/root/infobiotics/prebuild

INSTALLBASE=/usr
INSTALLLIB=${INSTALLBASE}/local/${PKGBASE}/lib
INSTALLBIN=${INSTALLBASE}/bin
OTOOL_LOCAL=otool
INSTALL_NAME_TOOL_LOCAL=install_name_tool
OTOOL=otool
INSTALL_NAME_TOOL=install_name_tool
EPMLIST=${PKGNAME}.list
EPMLIST=${PKGBASE}.list
EPMCOPYING=${PKGCONFDIR}/COPYING
EPMREADME=${PKGCONFDIR}/README
PRISMDIR=prism-3.3.1
PRISMTARBALL=prism-3.3.1-compiled.tar.gz

echo "building ${ARCH} package..."

# remove old builds
rm -rf ${BUILDTMP} ${PKGDIR}
mkdir ${BUILDTMP} ${PKGDIR} &> /dev/null

# build apple binary
pushd ${BUILDTMP} &> /dev/null
cat ${BUILDDIR}/${MANIFEST} |
while read package version
do
	if [ ${package} = "infobiotics-workbench" ]
	then
		continue
	fi
	echo "building ${package} ${version}..."
	# unpack tarball
	pkgbase=${package}-${version}
	tarball=${pkgbase}.tar.gz
	BUILDLOG=${BUILDTMP}/${pkgbase}.build.log
	if [ ! -e ${SOFTREPOSRC}/${tarball} ]
	then               
	        echo "error: couldn't find ${tarball}"
        	exit 1
	fi
	tar -xzvf ${SOFTREPOSRC}/${tarball} &> /dev/null
	if [ $? != 0 ]
	then
	        echo "error: couldn't unpack ${tarball}"
        	exit 1
	fi
	
	# set specific configuration args for programs
	EXTRA_ARGS=""
#	if [ ${package} = "mcss" ]
#	then
#		EXTRA_ARGS="--with-ecsb-exec=/usr/local/bin/ecsb-make-parameter-class"
#	fi

	# build packages
	pushd ${pkgbase} &> /dev/null &&

	if [ ${package} == "InfobioticsDashboard" ]
	then
#		export PATH=/Library/Frameworks/Python.framework/Versions/6.1/bin:$PATH
#		export ETS_TOOLKIT=qt4
		./make_app.sh &> ${BUILDLOG} &&
		cp -r dist/${package}.app ${PKGDIR} &> /dev/null
		if [ $? != 0 ]
		then
	        	echo "error: couldn't build ${pkgbase}"
	        	exit 1
		fi
	else
		# install to ARCHROOT
		./configure &> ${BUILDLOG} &&
		make all install &> ${BUILDLOG}
		if [ $? != 0 ]
		then
	        	echo "error: couldn't build ${pkgbase}"
	        	exit 1
		fi
	fi

	popd &> /dev/null
done
if [ $? != 0 ]
then
       	exit 1
fi

popd &> /dev/null

# make package
# copy files
echo "copying files..."
for i in $(cat ${FILELIST})
do
        TODIR=$(dirname $i) &&
        mkdir -p ${PKGDIR}/${TODIR} &&
        cp -r ${ARCHROOT}/$i ${PKGDIR}/${TODIR}/
	if [ $? != 0 ]
	then
        	echo "error: unable to copy file $i"
	       	exit 1
	fi
done
if [ $? != 0 ]
then
       	exit 1
fi

# adjust directories
mkdir -p ${PKGDIR}/local/${PKGBASE} &&
mv ${PKGDIR}/lib ${PKGDIR}/local/${PKGBASE}/ &&
mv ${PKGDIR}/share/doc ${PKGDIR}/local/${PKGBASE}/ &&
mkdir -p ${PKGDIR}/local/${PKGBASE}/bin &&
cp ${PKGDIR}/share/mc2*/* ${PKGDIR}/local/${PKGBASE}/bin/ &&
cp ${PKGCONFDIR}/COPYING ${PKGCONFDIR}/README ${PKGCONFDIR}/VERSION ${PKGDIR}/local/${PKGBASE}/ &&
rm -rf ${PKGDIR}/share
if [ $? != 0 ]
then
        echo "error: unable to make package filesystem"
       	exit 1
fi
echo ${VERSION} > ${PKGDIR}/local/${PKGBASE}/VERSION
cp ${SOFTREPOSRC}/${PRISMTARBALL} ${PKGDIR}/local/${PKGBASE}/

# fix library paths
echo "fixing library paths..."
FIND="${ARCHROOT}/lib" &&
REP=$(echo "/usr/local/${PKGBASE}/lib" | sed 's/\//\\\//g') &&
for i in $(grep -rsI "${FIND}" ${PKGDIR}/local/${PKGBASE}/lib | cut -f 1 -d ':')
do
	FIND=$(echo "${ARCHROOT}/lib" | sed 's/\//\\\//g') &&
        cat $i | sed "s/${FIND}/${REP}/g" > ${TMPFILE} &&
        mv $TMPFILE $i
	if [ $? != 0 ]
	then
        	echo "error: unable to fix path of $i"
	       	exit 1
	fi
done
if [ $? != 0 ]
then
       	exit 1
fi

# fix permissions
echo "fixing permissions..."
for i in $(find ${PKGDIR}/local/${PKGBASE}/lib -type f | egrep '\.dylib$')
do
        chmod a+rxw,go-w $i
	if [ $? != 0 ]
	then
        	echo "error: unable to fix permissions of $i"
	       	exit 1
	fi
done &&
for i in $(find ${PKGDIR}/local/${PKGBASE}/lib -type f | egrep '\.[l]a$')
do
        chmod u+rw,a-x,go-w $i
	if [ $? != 0 ]
	then
        	echo "error: unable to fix permissions of $i"
	       	exit 1
	fi
done
if [ $? != 0 ]
then
       	exit 1
fi

# fix libraries
echo "fixing library linking..."
FIND=$(echo "${ARCHLIB}" | sed 's/\//\\\//g') &&
for i in $(find ${PKGNAME}/local/${PKGBASE}/lib -type f | egrep '\.dylib')
do
        ${INSTALL_NAME_TOOL_LOCAL} -id ${INSTALLLIB}/$(basename $i) $i &&
        for j in $(${OTOOL_LOCAL} -L $i | grep "${ARCHROOT}" | sed 's/^\t//g' | cut -f 1 -d ' ')
        do
                REP=$(echo "${INSTALLLIB}" | sed 's/\//\\\//g') &&
                NEWLIB=$(echo $j | sed "s/${FIND}/${REP}/g") &&
                ${INSTALL_NAME_TOOL_LOCAL} -change $j ${NEWLIB} $i
		if [ $? != 0 ]
		then
        		echo "error: unable to fix library $i"
	       		exit 1
		fi
        done
	if [ $? != 0 ]
	then
	       	exit 1
	fi
done
if [ $? != 0 ]
then
       	exit 1
fi

# adjust executables
echo "fixing executable linking..."
FIND=$(echo "${ARCHLIB}" | sed 's/\//\\\//g') &&
for i in $(ls -1 ${PKGNAME}/bin/*)
do
        for j in $(${OTOOL_LOCAL} -L $i | grep "${ARCHROOT}" | sed 's/^\t//g' | cut -f 1 -d ' ')
        do
                REP=$(echo "${INSTALLLIB}" | sed 's/\//\\\//g') &&
                NEWLIB=$(echo $j | sed "s/${FIND}/${REP}/g") &&
                ${INSTALL_NAME_TOOL_LOCAL} -change $j ${NEWLIB} $i
		if [ $? != 0 ]
		then
        		echo "error: unable to fix executable $i"
			echo "command: ${INSTALL_NAME_TOOL_LOCAL} -change $j ${NEWLIB} $i"
	       		exit 1
		fi
        done
	if [ $? != 0 ]
	then
	       	exit 1
	fi
done
if [ $? != 0 ]
then
       	exit 1
fi

echo "creating control file..."
EPMDESCRIPTION="Infobiotics Workbench ${VERSION}." &&

# create epm control file
cat << EOF > ${BUILDDIR}/${EPMLIST}
%product ${PKGNAME}
%version ${VERSION}
%license ${EPMCOPYING}
%readme ${EPMREADME}
%description ${EPMDESCRIPTION}
%copyright 2008,2009,2010 Jamie Twycross, Francisco Romero Campero, Jonathan Blakes, Claudio Lima
%vendor Jamie Twycross, Francisco Romero Campero, Jonathan Blakes, Claudio Lima
%packager Jamie Twycross <jpt@cs.nott.ac.uk>
EOF
if [ $? != 0 ]
then
	echo "error: unable to create control file"
       	exit 1
fi

echo "creating package list..."
mkepmlist -g root -u root --prefix /usr ${PKGNAME} | sed 's/\/usr\/InfobioticsDashboard.app\//\/Applications\/Infobiotics\\ Dashboard.app\//g' | sed 's/\\\$/\\\$\$/g' >> ${BUILDDIR}/${EPMLIST}
if [ $? != 0 ]
then
        echo "error: unable to make package list"
        exit 1
fi

echo "creating postinstall script..."
cat << EOF2 >> ${BUILDDIR}/${EPMLIST}
%postinstall << EOF
cd /usr/local/${PKGBASE}
tar -xzvf ${PRISMTARBALL} &> /dev/null
rm -f ${PRISMTARBALL}
EOF
EOF2

# create package
echo "creating package..."
#epm -a i386 --output-dir . -v -g -f osx -n $PKGBASE &> build.log
cd ${BUILDDIR} &&
epm --output-dir . -v -g -f osx -n $PKGBASE &> epm.log
if [ $? != 0 ]
then
        echo "error: unable to build apple package"
        exit 1
fi

# tidy up
rm -rf ${BUILDTMP} ${PKGDIR} ${BUILDDIR}/${EPMLIST} ${PKGDIR}.pkg epm.log

echo "built ${ARCH} package successfully"

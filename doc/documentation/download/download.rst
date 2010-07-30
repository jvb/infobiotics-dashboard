Downloading and Installing
==========================

The Infobiotics Workbench is composed of four components:  the ``infobiotics-dashboard`` graphical workflow manager; the ``mcss`` multicompartment stochastic simulator; the ``pmodelchecker`` probabilistic model checker; and the ``poptimizer`` structure and parameter optimizer. We recommend that you install the latest ``infobiotics-workbench`` package for your platform, which will automatically install all of these components, although each component can be installed independently if required.

Precompiled binaries are available for a number of platforms or you can download the source code and compile it yourself. Please follow the link below for instructions on downloading and installing for your particular platform. If you experience any problems installing the Workbench please have a look at the Infobiotics Workbench `FAQ <http://getsatisfaction.com/infobiotics/products/infobiotics_infobiotics_workbench>`_ first, and if you are still stuck drop us a message by pressing the Feedback button at the left of this page.

- `Linux Debian/Ubuntu deb packages`_
- `Linux Fedora/CentOS/SUSE rpm packages`_
- `Linux statically-compiled binaries`_
- `Macintosh binary package`_
- `Windows binary package`_
- `Source code`_

Linux Debian/Ubuntu deb packages
################################

Linux binary and source code packages are available from the Infobiotics apt repository. Currently, binary packages are available for i386 and x86_64 (e.g. amd64) architectures. To use the repository you need to add the following lines to your /etc/apt/sources.list file or to the list of repositories in your graphical package manager::

	deb http://www.infobiotic.net/infobiotics-apt stable contrib
	deb-src http://www.infobiotic.net/infobiotics-apt stable contrib

Then update your package list by typing (as root)::

	$ apt-get update

Then to install the latest version of the complete Infobiotics Workbench type::

	$ apt-get install infobiotics-workbench

This will install all the necessary components for the Workbench. If you prefer to install individual components instead of the whole Workbench then simply install the corresponding individual packages. For example, to install the multicompartment stochastic simulator (mcss) type::

	$ apt-get install mcss

Following the above instructions will always mean you get the latest version of the Workbench. We also provide the facility to install specific versions of the Workbench and its components. For example, to install version 0.0.2 of the Workbench, type::

	$ apt-get install infobiotics-workbench-0.0.2

Source code for the Workbench and its components can also be downloaded e.g. typing::

	$ apt-get source mcss-0.0.30

Will download a tarball of the source code for mcss version 0.0.30 and unpack it in your current working directory.

All packages in the repository are signed with the Infobiotics GPG key. If you want to install the Infobiotics repository keyring so that you do not have to authorise package installation each time then install the ``infobiotics-keyring`` package by typing::

	$ apt-get install infobiotics-keyring

Below is a list of all the packages in the repository. We also provide binary packages for some 3rd party software which is used by the Workbench.

+-----------------------+-----------------------------------------------------------------+
| Package               | Description                                                     |
+=======================+=================================================================+
| infobiotics-workbench | Metapackage which installs all Infobiotics Workbench components |
+-----------------------+-----------------------------------------------------------------+
| mcss                  | P system multicompartment stochastic simulator                  |
+-----------------------+-----------------------------------------------------------------+
| poptimizer            | P system parameter optimizer                                    |
+-----------------------+-----------------------------------------------------------------+
| pmodelchecker         | P system model checker                                          |
+-----------------------+-----------------------------------------------------------------+
| libecsb               | Library for executable cell systems biology                     |
+-----------------------+-----------------------------------------------------------------+
| python-mcss           | Python bindings for the multicompartment stochastic simulator   |
+-----------------------+-----------------------------------------------------------------+
| infobiotics-keyring   | GPG keyring for the Infobiotics repository                      |
+-----------------------+-----------------------------------------------------------------+
| libhdf5-serial-1.8.3  | HDF5_ library (3rd party)                                       |
+-----------------------+-----------------------------------------------------------------+
| libsbml-4.0.0         | SBML_ library (3rd party)                                       |
+-----------------------+-----------------------------------------------------------------+
| mc2-2.0beta2          | MC2_ model checker (3rd party)                                  |
+-----------------------+-----------------------------------------------------------------+
| prism-3.3.beta2       | Prism_ model checker (3rd party)                                |
+-----------------------+-----------------------------------------------------------------+

.. _HDF5: http://www.hdfgroup.org/HDF5/
.. _SBML: http://sbml.org/Software/libSBML
.. _MC2: http://www.brc.dcs.gla.ac.uk/software/mc2/
.. _Prism: http://www.prismmodelchecker.org/

Linux Fedora/CentOS/SUSE rpm packages
#####################################

Binary i386 and x86_64 rpm packages are available from a yum repository. All packages in the repository are signed with the Infobiotics GPG key. To use the repository add the following lines to your /etc/yum.conf file::

	[infobiotics]
	name=Infobiotics Workbench $basearch
	baseurl=http://www.infobiotic.net/infobiotics-yum/$basearch
	enabled=1
	gpgcheck=1
	gpgkey=http://www.infobiotic.net/infobiotics-yum/public.gpg

You should now be able to install the complete Infobiotics Workbench by typing::

	$ yum install infobiotics-workbench

This will install all the necessary components for the Workbench. If you want to install individual components instead of the whole Workbench then just install their individual packages e.g. to install the multicompartment stochastic simulator (mcss) type::

	$ yum install mcss

Following the above instructions will always mean you get the latest version of the Workbench. We also provide the facility to install specific versions of the Workbench and its components. For example, to install version 0.0.2 of the Workbench, type::

	$ yum install infobiotics-workbench-0.0.2

The repository can be browsed and packages downloaded individually by visiting:

	http://www.infobiotics.org/infobiotics-yum/

Below is a list of all the packages in the repository. We also provide binary packages for some 3rd party software which is used by the Workbench.

+-----------------------+-----------------------------------------------------------------+
| Package               | Description                                                     |
+=======================+=================================================================+
| infobiotics-workbench | Metapackage which installs all Infobiotics Workbench components |
+-----------------------+-----------------------------------------------------------------+
| mcss                  | P system multicompartment stochastic simulator                  |
+-----------------------+-----------------------------------------------------------------+
| poptimizer            | P system parameter optimizer                                    |
+-----------------------+-----------------------------------------------------------------+
| pmodelchecker         | P system model checker                                          |
+-----------------------+-----------------------------------------------------------------+
| libecsb               | Library for executable cell systems biology                     |
+-----------------------+-----------------------------------------------------------------+
| python-mcss           | Python bindings for the multicompartment stochastic simulator   |
+-----------------------+-----------------------------------------------------------------+
| infobiotics-keyring   | GPG keyring for the Infobiotics repository                      |
+-----------------------+-----------------------------------------------------------------+
| libhdf5-serial-1.8.3  | HDF5_ library (3rd party)                                       |
+-----------------------+-----------------------------------------------------------------+
| libsbml-4.0.0         | SBML_ library (3rd party)                                       |
+-----------------------+-----------------------------------------------------------------+
| mc2-2.0beta2          | MC2_ model checker (3rd party)                                  |
+-----------------------+-----------------------------------------------------------------+
| prism-3.3.beta2       | Prism_ model checker (3rd party)                                |
+-----------------------+-----------------------------------------------------------------+

Linux statically-compiled binaries
##################################

Linux 32- and 64-bit statically-compiled executables are available for all of the Infobiotics Workbench components. These executables should work on all recent Linux systems, and can be downloaded from:

	http://www.infobiotics.org/infobiotics-software/binary/

Download the latest tarball for your platform, unpack it and inside the directory that is created you will find the executables and documentation for all the Workbench components.

Macintosh binary package
########################

A binary package is available for Mac OS X 10.6 (Snow Leopard). This package will install the Infobiotics Workbench and all its components. First, download the latest dmg disk image  (infobiotics-workbench-X.X.X.dmg) from:

	http://www.infobiotics.org/infobiotics-software/apple/

Once downloaded, double click on the .dmg file to mount it. In the window that appears double click on the .pkg file and follow the on-screen instructions.

Windows binary package
######################

A binary installer package and zip package are available for Windows. We recommend that you use the binary installer package. The installer will install the Infobiotics Workbench and all its components. Download the latest installer file (Infobiotics-Workbench-Setup-X.X.X-Setup.exe) from:

	http://www.infobiotics.org/infobiotics-software/windows/

Once downloaded, double click on the file to run it and follow the on-screen instructions.

If you prefer to use the zip package, then download the latest zip package (Infobiotics-Workbench-X.X.X.zip) from the above location and unzip it to a location of your choice. Inside the directory that is created you will find executables and documentation for all the Workbench components.

Source code
############

The source code for the Infobiotics Workbench and all its components is licensed under the open source GNU GPL V3 license and is available for download from:

	http://www.infobiotics.org/infobiotics-software/src/

Please read the README file contained in the source tarball of each component for compilation and installation instructions.

The source code for the 3rd party software included in the binary distributions of the Workbench is available here:

	http://www.infobiotics.org/infobiotics-software/contrib/

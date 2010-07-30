Downloading Infobiotics Workbench
=================================

Precompiled binaries are available for a number of platforms or you can download the source code:

- `Linux Debian/Ubuntu packages`_
- `Macintosh binary package`_
- `Windows binary package`_
- `Source code`_

If you have any problems installing the Workbench please have a look at the Installation FAQ and Infobiotics Workbench List first, and if you're still stuck then post a message.

Linux Debian/Ubuntu packages
############################

Linux binary and source code packages are available from the Infobiotics APT repository. Currently, binary packages are available for i386 and x86_64 (e.g. amd64) architectures. To use the repository you need to add the following lines to your /etc/apt/sources.list file or to the list of repositories in your graphical package manager::

	deb http://www.infobiotic.net/infobiotics-repository stable contrib
	deb-src http://www.infobiotic.net/infobiotics-repository stable contrib

Then update your package list by, for example, typing (as root)::

	$ apt-get update

Then to install the latest version of the Infobiotics Workbench install the ``infobiotics-workbench`` package e.g.::

	$ apt-get install infobiotics-workbench

This will install all the necessary components for the Workbench. If you want to install individual components instead of the whole Workbench then just install their individual packages e.g. to install the multicompartment stochastic simulator (mcss) type::

	$ apt-get install mcss

Following the above instructions will always mean you get the lastest version of the Workbench. We also provide the facility to install specific versions of the Workbench and its components. For example, to install version 0.0.30 of mcss, type::

	$ apt-get install mcss-0.0.30

Source code for the Workbench and its components can also be downloaded e.g.::

	$ apt-get source mcss

Will download a tarball of the lastest source code for mcss and unpack it in your current working directory.

All packages in the repository are signed with a GPG key. If you want to install the Infobiotics repository keyring so that you don't have to authorise package installation each time then install the ``infobiotics-keyring`` package e.g.::

	$ apt-get install infobiotics-keyring

Below is a list of all the packages in the repository. We also provide binary and source code packages for some 3rd party software which is used by the Workbench.

+-----------------------+---------------------------------------------------------------+
| Package               | Description                                                   |
+=======================+===============================================================+
| infobiotics-workbench | Graphical user interface for the Workbench components         |
+-----------------------+---------------------------------------------------------------+
| mcss                  | P system multicompartment stochastic simulator                |
+-----------------------+---------------------------------------------------------------+
| poptimizer            | P system parameter optimizer                                  |
+-----------------------+---------------------------------------------------------------+
| pmodelchecker         | P system model checker                                        |
+-----------------------+---------------------------------------------------------------+
| libecsb               | Library for executable cell systems biology                   |
+-----------------------+---------------------------------------------------------------+
| python-mcss           | Python bindings for the multicompartment stochastic simulator |
+-----------------------+---------------------------------------------------------------+
| infobiotics-keyring   | GPG keyring for the Infobiotics repository                    |
+-----------------------+---------------------------------------------------------------+
| libhdf5-serial-1.8.3  | HDF5_ library (3rd party)                                     |
+-----------------------+---------------------------------------------------------------+
| libsbml-4.0.0         | SBML_ library (3rd party)                                     |
+-----------------------+---------------------------------------------------------------+
| mc2-2.0beta2          | MC2_ model checker (3rd party)                                |
+-----------------------+---------------------------------------------------------------+
| prism-3.3.beta2       | Prism_ model checker (3rd party)                              |
+-----------------------+---------------------------------------------------------------+

.. _HDF5: http://www.hdfgroup.org/HDF5/
.. _SBML: http://sbml.org/Software/libSBML
.. _MC2: http://www.brc.dcs.gla.ac.uk/software/mc2/
.. _Prism: http://www.prismmodelchecker.org/

Macintosh binary package
########################

Coming soon.

Windows binary package
######################

Coming soon.

Source code
############

The source code for the Infobiotics Workbench and all its components is licensed under the open source GNU GPL V3 license and is available for download from http://www.infobiotics.org/infobiotics-src/. The source code for the 3rd party software included in the binary distributions of the Workbench is available in the contrib_ subdirectory.

.. _contrib: http://www.infobiotics.org/infobiotics-src/contrib
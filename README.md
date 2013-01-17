infobiotics-dashboard
=====================

Infobiotics Dashboard is the front to the Infobiotics Workbench.

The previous release of Infobiotics Dashboard hosted on [bitbucket](https://bitbucket.org/jvb/infobiotics-dashboard) was compatible only with Traits 3, which was superceded in recent releases of Ubuntu/Debian (Linux) and the Enthought Tool Suite/python-xy (Windows/Mac).

This release is compatible only with Traits 4.

Installing
----------

### From source

1. Either clone this repository or download the zip above.
2. From the cloned repository/unzipped directory run:

<!--
	./sdist.sh
	cd dist/Infobiotics-Dashboard-1.1.0/
	python setup.py install
 -->

	python setup.py install

which should install all of the necessary Python packages from PyPI.

#### Ubuntu/Debian dependencies

If you prefer to let the system handle your Python packages:

	apt-get install python-qt4 mayavi2 python-tables python-matplotlib python-scipy python-configobj python-pexpect python-progressbar python-setproctitle python-xlwt

The Python package [Quantities](http://packages.python.org/quantities/user/tutorial.html) 
does not have a package in the repository,
so we provide a [.deb](https://bitbucket.org/jvb/infobiotics-dashboard/downloads/python-quantities_0.9.0-1_all.deb)
that can be installed with:

	wget https://bitbucket.org/jvb/infobiotics-dashboard/downloads/python-quantities_0.9.0-1_all.deb
	dpkg -i python-quantities_0.9.0-1_all.deb








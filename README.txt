
=====================
Infobiotics Dashboard
=====================

Copyright 2008, 2009, 2010 Jonathan Blakes, jvb@cs.nott.ac.uk
Released under GNU GPL version 3.


Dependencies
============

This software has the following dependencies:

* Python >= 2.6 (http://www.python.org/)
* HDF5 >= 1.8 (http://www.hdfgroup.org/HDF5/)
* VTK >= 5.2 (http://www.vtk.org/)

* NumPy >= 1.2.1 (http://numpy.scipy.org/)
* Matplotlib >= 99.1 (http://matplotlib.sourceforge.net/)

All of the above dependencies can be fulfilled by installing the Enthought
Python Distribution (http://www.enthought.com/products/epd.php).


* Qt >= (http://qt.nokia.com/)
* PyQt >= 4.7(http://www.riverbankcomputing.co.uk/software/pyqt/)
* QScintilla2 (http://www.riverbankcomputing.co.uk/software/qscintilla/download)

On Windows all of the above dependencies can be fulfilled by installing the 
Basic and Advanced Python modules of Python(x,y) (http://www.pythonxy.com/).


* Infobiotics Workbench (http://www.infobiotic.org/infobiotics-workbench)

On Debian-based GNU/Linux systems all of the above dependencies can be 
fulfilled by adding the APT line:

http://www.infobiotic.net/infobiotics-apt

to /etc/apt/sources.list and in a terminal:

$ sudo apt-get install infobiotics-workbench python-vtk python-qt4 python-qscintilla2

NumPy must be installed with either: 

$ pip install numpy

or

$ easy_install numpy

Matplotlib must be similarly be installed with:

& pip install http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-0.99.1/matplotlib-0.99.1.2.tar.gz/download 


Installation
============

Unpacked the downloaded archive and in a terminal:

$ python setup.py install

or

$ pip install --upgrade InfobioticsDashboard-<version>.<archive-format>

which will install the Infobiotics Dashboard and the latest versions of 
PyTables (http://www.pytables.org/), 
most of the Enthought Tool Suite (http://www.enthought.com/products/ets.php) 
and a few other packages from the Python Package Index 
(http://pypi.python.org/pypi).


Running
=======

To run the Infobiotics Dashboard at the terminal type:

$ infobiotics-dashboard.py

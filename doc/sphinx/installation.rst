Installation
============

.. topic:: Section summary

    This section details the various ways of installing and compiling 
    Infobiotics Dashboard. It is shamelessly adapted from the `Mayavi 
    installation documentation 
    <http://code.enthought.com/projects/mayavi/docs/development/html/mayavi/installation.html>`_.

    If you already have Infobiotics Dashboard up and running, you can skip 
    this section.

.. Up-to-date install instructions for the latest version of Infobiotics 
Dashboard are always available from links at the `Infobiotics trac wiki 
<https://psiren.cs.nott.ac.uk/projects/infobiotics>`_.  The following will 
give you a good idea of the general installation procedure and a start on 
where to look for more information.


Follow the `instructions for installing the Infobiotics Workbench 
<http://www.infobiotics.org/infobiotics-workbench/download/download.html>`_.  
	
	

	* Linux
		* Debian/Ubuntu
		* Fedora/RedHat
	
	* Source
	* 
	


Dependencies
------------

Infobiotics Dashboard depends on the the following software (versions) to 
function: 
    * Qt (>=4.4)
    * QScintilla2 (>=2)
    * PyQt (>=4.4)
    * HDF5 (1.6/1.8)
    * Python-2.x (x>=5)
    * NumPy (>=1.2.1)
    * PyTables (>=2.1.1)
    * Matplotlib (>=0.98)
    * VTK (>=5.2)
    * Enthought Tool Suite (>=3.1) - Mayavi2, Traits and TraitsUI, Envisage
    * Infobiotics Workbench (mcss, pmodelchecker, poptimizer) 

Fortunately in most circumstances some of these can be provided by one or more 
of the following methods:
	* scientific Python distributions: 
		* Python(x,y) on Windows
		* EPD on Windows, MacOS and Linux
	* Linux package management systems:
		* APT on Debian/Ubuntu/etc
		* YUM on Fedora/CentOS/etc
	* Python Package Index (PyPI) via *easy_install*

.. NumPy, PyTables, Matplotlib and ETS can be easy_install'd if setuptools is installed.

.. _Infobiotics:	http://www.infobiotic.org/
.. _HDF5: 			http://www.hdfgroup.org/HDF5/
.. _Python: 		http://www.python.org/
.. _NumPy: 			http://numpy.scipy.org/
.. _PyTables: 		http://www.pytables.org/
.. _Qt: 			http://qt.nokia.com/
.. _PyQt: 			http://www.riverbankcomputing.co.uk/software/pyqt/
.. _Matplotlib: 	http://matplotlib.sourceforge.net/
.. _ET S:			http://www.enthought.com/products/ets.php



Installing ready-made distributions
------------------------------------

:Windows:
     Under Windows the best way to install the dependencies of Infobiotics 
     Dashboard is to install a full Python distribution, such as `Python(x,y) 
     <http://www.pythonxy.com/>`_ or the `Enthought Python Distribution (EPD) 
     <http://www.enthought.com/products/epd.php>`_. 
     
     :Python(x,y):
	     Python(x,y), you need to check install the *Full Edition* **or** 
	     choose to perform a *custom installation* and check *ETS, PyTables, 
	     matplotlib* when selecting 
	     components. If you want to reduce the disk used by the Python(x,y), you 
	     can uncheck other components such as Eclipse_. 
     
     
     
:MacOSX:
    The full Python distribution EPD_ (that includes Mayavi) is also
    available for MacOSX.  Unless you really enjoy the intricacies of
    compilation, this is the best solution to install Mayavi.

:Ubuntu or Debian:
     Mayavi is packaged in Debian and Ubuntu. In addition, more up to
     date packages of Mayavi releases for old versions of Ubuntu are
     available at https://launchpad.net/~gael-varoquaux/+archive .
     Experimental Debian packages are also available at
     http://people.debian.org/~varun/ .

:RedHat EL3 and EL4:
    The full Python distribution EPD_ (that includes Mayavi) is also
    available for RHEL3 and 4.


Requirements for manual installs
--------------------------------

If you are not using a full, ready-made, scientific Python distribution, you need to satistify Mayavi's requirements (for a step-by-step guide on installing all these under windows, see :ref:`below <step-by-step-window-installation>`).

Mayavi requires at the very minimum the following packages:

    * VTK_ >= 4.4 (5.x is ideal)
    * numpy_ >= 1.0.1
    * setuptools_ (for installation and egg builds)
    * Traits_ >= 3.0 (`Traits`, `TraitsGUI` and `TraitsBackendWX` or
      `TraitsBackendQt`, `EnthoughtBase`, `AppTools`)
      **Note** Depending on your installation
      procedure, you might not need to instal manually these
      requirements.

The following requirements are really optional but strongly recommended,
especially if you are new to Mayavi:

    * wxPython_ 2.8.x
    * configobj_
    * Envisage_ == 3.x (`EnvisageCore` and `EnvisagePlugins`) 
      **Note** These last requirements can be automatically installed,
      see below.

One can install the requirements in several ways.  

   * Windows and MacOSX: even if you want to build from source, a good
     way to install the requirements is to install one of the
     distributions indicated above. Note that under Windows, EPD_ comes
     with a compiler (mingw) and facilitates building Mayavi.

   * Linux: Most Linux distributions will have installable binaries
     available for the some of the above.  For example, under Debian_ or
     Ubuntu_ you would need ``python-vtk``, ``python-wxgtk2.6``,
     ``python-setuptools``, ``python-numpy``, ``python-configobj``.
     More information on specific distributions and how you can get the
     requirements for each of these should be available from the list of
     distributions here:

        https://svn.enthought.com/enthought/wiki/Install

   * Mac OS X: The best available instructions for this platform are
     available on the IntelMacPython25_ page.


There are several ways to install TVTK_, Traits_ and Mayavi.  These are described in the following.

.. _TVTK: https://svn.enthought.com/enthought/wiki/TVTK
.. _VTK: http://www.vtk.org
.. _envisage: https://svn.enthought.com/enthought/wiki/Envisage
.. _Traits: https://svn.enthought.com/enthought/wiki/Traits
.. _wxPython: http://www.wxpython.org
.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
.. _enstaller: http://code.enthought.com/enstaller
.. _Debian: http://www.debian.org
.. _Ubuntu: http://www.ubuntu.com
.. _IntelMacPython25: https://svn.enthought.com/enthought/wiki/IntelMacPython25
.. _EPD: http://www.enthought.com/products/epd.php
.. _Eclipse: http://www.eclipse.org/downloads/
.. _configobj: http://pypi.python.org/pypi/ConfigObj/

Doing it yourself: Python packages: Eggs
-----------------------------------------

Installing with `easy_install`
...............................

First make sure you have the prerequisites for Mayavi installed, as
indicated in the previous section, i.e. the following packages:

    * VTK_ >= 4.4 (5.x is ideal)
    * numpy_ >= 1.0.1
    * wxPython_ >= 2.8.0
    * configobj_
    * setuptools_ (for installation and egg builds; later the better)

Mayavi_ is part of the Enthought Tool Suite (ETS_).  As such, it is
distributed as part of ETS and therefore binary packages and source
packages of ETS will contain Mayavi. Mayavi releases are almost always
made along with an ETS release.  You may choose to install all of ETS or
just Mayavi alone from a release. 

ETS has been organized into several different Python packages.  These
packages are distributed as Python Eggs_.  Python eggs are fairly
sophisticated and carry information on dependencies with other eggs.  As
such they are rapidly becoming the standard for distributing Python
packages.

The easiest way to install Mayavi with eggs is to use pre-built eggs 
built for your particular platform and downloaded by `easy_install`. 
Alternatively `easy_install` can build the eggs from the source tarballs.
This is also fairly easy to do if you have a proper build environment.

To install eggs, first make sure the essential requirements are
installed, and then build and install the eggs like so::

 $ easy_install "Mayavi[app]" 

This one command will download, build and install all the required ETS
related modules that Mayavi needs for the latest ETS release, this means
that the `Traits` dependencies and the `Envisage` dependencies will be
installed automatically. If you run into trouble please check the
`Enthought Install`_ pages.

One common sources of problems during an install, is the presence of
older versions of packages such as Traits, Mayavi, Envisage or TVTK.
Make sure that you clean your ``site-packages`` before installing a new
version of Mayavi. Another problem often encountered is running into
what is probably a bug of the build system that appears as a "sandbox
violation". In this case, it can be useful to try the download and
install command a few times.

If you still have problems, given this background, please see the
following `Enthought Install`_ describes how ETS can be installed
with eggs. Check this page first.  It contains information on how to
install the prebuilt binary eggs for various platforms along with any
dependencies.


.. note:: Automatic downloading of required eggs

    If you whish to download all the eggs fetched by `easy_install`, for
    instance to propagate to an offline PC, you can use virtualenv to
    create an empty site-packages, and install to it::

        virtualenv --no-site-packages temp
        cd temp
        source bin/activate
        mkdir temp_subdir
        easy_install -zmaxd temp_subdir "Mayavi[app,nonets]"


.. _step-by-step-window-installation:

Step-by-step instructions to install with eggs under Windows
...............................................................

If you do not wish to install a ready-made distribution under Windows,
these instructions (provided by Guillaume Duclaux) will guide you through
the necessary steps to configure a Windows environment in which Mayavi
will run.

1. Install Python 2.5. Add 'C:\\Python25;` to the PATH environment
   variables.

2. Install Mingw32, from the Download section of http://www.mingw.org/ ,
   use the MinGW5.1.4 installer. Add 'C:\\MinGW\\bin;' to the PATH
   environment variables.

3. Create a 'c:\\documents and settings\\USERNAME\\pydistutils.cfg' file(where 
   USERNAME is the login) with the following contents::

               [build]
               compiler=mingw32

4. Create the new environment variable HOME and set it to the value:
   'c:\\docume~1\\USERNAME;' (where USERNAME is the login name)

5. Install Setuptools (0.6c9 binary) from its webpage, and
   'C:\Python25\Scripts;' to the PATH environment variables

6. Install VTK 5.2 (using Dr Charl P. Botha Windows binary
   http://cpbotha.net/2008/09/23/python-25-enabled-vtk-52-windows-binaries/
   )

    * Unzip the folder content in 'C:\\Program Files\\VTK5.2_cpbotha'
    * add 'C:\\Program Files\\VTK5.2_cpbotha\\bin;' to the PATH environment
      variables
    * create a new environment variable PYTHONPATH and set it to the
      value 'C:\\Program Files\\VTK5.2_cpbotha\\lib\\site-packages;'
    * If you are running an old version of windows (older than XP)
      download msvcr80.dll and msvcp80.dll from the www.dll-files.com
      website and copy them into C:\\winnt\\system32.

7. Install Numpy (binary from http://numpy.scipy.org/ )

8. Installing wxPython (2.8 binary from http://www.wxpython.org/ )

9. Run in cmd.exe::

     easy_install Sphinx EnvisageCore EnvisagePlugins configobj

10. Finally, run in cmd.exe::

     easy_install Mayavi[app]


.. _Eggs: http://peak.telecommunity.com/DevCenter/PythonEggs
.. _Enthought Install: https://svn.enthought.com/enthought/wiki/Install
.. _ETS: http://code.enthought.com/ets

.. _installing_svn:

Under Mac OSX Snow Leopard
-------------------------------

Under Mac OSX Snow Leopard, you may need to build VTK yourself. Here are
instructions specific to Snow Leopard (thanks to Darren Dale for
providing the instructions):

#. Download the VTK tarball, unzip it, and make a build directory
   (vtkbuild) next to the resulting VTK directory

#. Then cd into vtkbuild and run "cmake ../VTK". Next, edit CMakeCache.txt 
   (in vtkbuild) and set::

      //Build Verdict with shared libraries.
      BUILD_SHARED_LIBS:BOOL=ON

      //Build architectures for OSX
      CMAKE_OSX_ARCHITECTURES:STRING=x86_64

      //Minimum OS X version to target for deployment (at runtime); newer
      // APIs weak linked. Set to empty string for default value.
      CMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.6

      //Wrap VTK classes into the Python language.
      VTK_WRAP_PYTHON:BOOL=ON

      //Arguments passed to "python setup.py install ..." during installation.
      VTK_PYTHON_SETUP_ARGS:STRING=

#. Run "cmake ../VTK" again.

#. Run "make -j 2" for a single cpu system. "make -j 9" will compile
   faster on an 8-core system.

#. Run "sudo make install"

#. Edit your ~/.profile and add the following line::

      export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/usr/local/lib/vtk-5.4

#. Run "source ~/.profile" or open a new terminal so the DYLD_LIBRARY_PATH
   environment variable is available.

#. After that, install Mayavi in the usual way.


The bleeding edge: SVN
----------------------

If you want to get the latest development version of Mayavi (e.g. for
developing Mayavi or contributing to the documentation), we
recommend that you check it out from SVN.  Mayavi depends on several
packages that are part of ETS.  It is highly likely that the
in-development mayavi version may depend on some feature of an as yet
unreleased component.  Therefore, it is very convenient to get all the
relevant ETS projects that mayavi recursively depends on in one single
checkout.  In order to do this easily, Dave Peterson has created a
package called ETSProjectTools_.  This must first be installed and then
any of ETS related repositories may be checked out.  Here is how you can
get the latest development sources.

 #. Make sure there is no other ETS package installed in your pythonpath::

     $ python
     >>> import enthought
     Traceback (most recent call last):
       File "<stdin>", line 1, in <module>
     ImportError: No module named enthought

    If you *don't* get the ImportError (e.g. importing ``enthought`` succeeds),
    then there is no way to install the svn Mayavi version over it (even if you
    put it first in your PYTHONPATH), because the older (setuptools managed)
    ETS packages will get picked up too and they will mess up things. This
    behavior might be surprising if you are new to setuptools.

    So for example if you use Ubuntu or Debian, you need to first remove all ETS 
    packages (in Ubuntu 9.04, you need to remove all of these: ``mayavi2 python-apptools
    python-enthoughtbase python-envisagecore python-envisageplugins
    python-traits python-traitsbackendwx python-traitsgui``).

 #. Install ETSProjectTools_ like so::

     $ svn co https://svn.enthought.com/svn/enthought/ETSProjectTools/trunk \
            ETSProjectTools
     $ cd ETSProjectTools
     $ python setup.py install

    This will give you the useful scripts ``ets``.  For more details on
    the tool and various options check the ETSProjectTools_ wiki page.

 #. To get just the sources for mayavi and all its dependencies do this::

      $ ets co "Mayavi[app]"

    This will look at the latest available mayavi, parse its ETS
    dependencies and check out the relevant sources.  If you want a
    particular mayavi release you may do::

      $ ets co "Mayavi[app]==3.0.1"

    If you'd like to get the sources for an entire ETS release do this
    for example::

      $ ets co "ets==3.0.2"

    This will checkout all the relevant sources from SVN.  Be patient,
    this will take a while.  More options for the ``ets`` tool are
    available in the ETSProjectTools_ page.

 #. Once the sources are checked out you may enter the checked-out
    directory, for example:: 

       $ cd Mayavi_3.3.1/

    and either:

    #. Install a development version, to track changes to SVN easily
       (recommended)::

        $ ets develop

       This will  install all the checked out sources via a ``setup.py
       develop`` applied to each package.  

       ..  note::

        To install of the packages in a different location than the
        default one, eg '~/usr/', use the following syntax::

            ets develop -c"--prefix ~/usr"

        make sure that the corresponding site-packages folder is in your 
        PYTHONPATH environment variable (for the above example it would
        be: '~/usr/lib/python2.x/site-packages/'

    #. Or build binary eggs of the sources to install localy::

        $ cd Mayavi_3.3.1
        $ ets bdist

       This will build all the eggs and put them inside a ``dist``
       subdirectory.  Run ``ets bdist -h`` for more bdist related options.
       The mayavi development egg and its dependencies  may be installed
       via::

        $ easy_install -f dist "Mayavi[app]"

    #. Alternatively, if you'd like just ``Mayavi`` installed via
       ``setup.py develop`` with the rest as binary eggs you may do::

        $ cd Mayavi_x.y.z
        $ python setup.py develop -f ../dist

       This will pull in any dependencies from the built eggs.

You should now have the latest version of Mayavi installed and usable.

.. _ETSProjectTools: https://svn.enthought.com/enthought/wiki/SVNScripts 


Testing your installation
-------------------------

The easiest way to test if your installation is OK is to run the mayavi2
application like so::

 mayavi2

To get more help on the command try this::

 mayavi2 -h

``mayavi2`` is the mayavi application.  On some platforms like win32
you will need to double click on the ``mayavi2.exe`` program found in
your ``Python2X\Scripts`` folder.  Make sure this directory is in your
path.

.. note::
  Mayavi can be used in a variety of other ways but the ``mayavi2``
  application is the easiest to start with.

If you have the source tarball of mayavi or have checked out the sources
from the SVN repository, you can run the examples in
``enthought.mayavi*/examples``.  There are plenty of example scripts
illustrating various features.  Tests are available in the
``enthought.mayavi*/tests`` sub-directory.


Troubleshooting
----------------

If you are having trouble with the installation you may want to check
the :ref:`getting-help` page for more details on how you can search for
information or email the mailing list.

..
   Local Variables:
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:

.. toctree::

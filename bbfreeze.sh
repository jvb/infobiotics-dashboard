#!/bin/sh

# 

echo <<HERE
http://markmail.org/message/5xcwd5yw7zl7ii77

Subject:	[Enthought-Dev] Standalone Envisage/Task application (Linux)	permalink
From:	Eraldo Pomponi (eral...@gmail.com)
Date:	Oct 11, 2011 7:52:53 am
List:	com.enthought.mail.enthought-dev

Dear all,

I would like to report what has been my experience compiling an Envisage/Task application. My target were to produce a binary for a Linux machine so I was looking for a tool that could fit my needs. I started with Pyinstaller (1.5.1) because of its documentation than I tested cx-freeze and bb-freeze.

Pyinstaller: FAILURE After a long time spent to write new "hooks" and tweaking pyface internals to deal with default resource (i.e. application standard image etc.) when the program is frozen, I were able to start the application but all the buttons were just unusable because they were completely white.

cx-freeze: FAILURE In this case I just tried the default command then I moved to bb-freeze that, as far as I know, is the cxfreeze evolution to some extent:

cxfreeze "application_main/script.py" --target-dir dist

############################################## bb-freeze: SUCCESSFUL ##############################################

Whit bb-freeze I finally got a working binary that I successfully tested on others machine. Some hints to get bb-freeze produce a useful result:

- Place the "main.py" script in the root of your project and avoid relative imports (in the whole project)

- Place in the top lines of your main script before any other imports:

import sip sip.setapi('QString', 2) sip.setapi('QVariant', 2)

To fix the annoying problem with different api version and:

def __dependencies_for_freezing(): from PyQt4 import QtGui, QtCore, QtOpenGL, QtNetwork import pyface.ui.qt4.resource_manager import pyface.ui.qt4.tasks.task_window_backend

To fix some dependency that bb-freeze is not able to find by itself.

- Copy all resources like "app_preference.ini" in the root where the binary have been created (e.g. dist/ ) and adjust your code so that it checks also the sys.executable directory to find what it needs (resources).

And that's it ... Your binary should be created and run as expected. For sure there are better approaches than mine so I will appreciate If someone would suggest a "better" way to do that.

Cheers, Eraldo

P.S. My app includes ObsPy too but I were unable to get it run . It compiles fine and also the dependent library are included properly but it rise an Exception at runtime (i.e. involving "package_res: " ) . Suggestions are welcome. 
HERE


echo "freezing with bbfreeze"
echo


# cleaning

# remove PKG_INFO, setup.cfg, .pyc and .class files; build, debian, dist and tmp directories; Debian packages; distribute and InfobioticsDashboard eggs  
./clean.sh


# pre-freezing

# make files executable
#TODO chmod +x bin/*

# set environment variables
export ETS_TOOLKIT=qt4

# install bbreeze (using pip)
##TODO easy_install pip
#TODO apt-get install python-pip 
#TODO pip install bbfreeze


# freezing

# run bbreeze
python freeze.py


# post-freezing

# add TVTK classes zip file to library; fixes: 'ImportError: TVTK not built properly. Unable to find either a directory: /home/jvb/git/infobiotics-dashboard/dist/library.zip/tvtk/tvtk_classes or a file: /home/jvb/git/infobiotics-dashboard/dist/library.zip/tvtk/tvtk_classes.zip with the TVTK classes.'
#./clean.sh && python freeze.py && unzip dist/library.zip -d dist/library/ && unzip /usr/lib/python2.7/dist-packages/tvtk/tvtk_classes.zip -d dist/library/tvtk/tvtk_classes/ && rm dist/library.zip && cd dist/library/ && (sudo zip -r ../library.zip * | grep denied) && cd ../.. && rm -rf dist/library/ && dist/infobiotics-dashboard && echo ok
cp -r tvtk_/ dist/tvtk/ && cd dist && zip library.zip tvtk/*.py && cd .. && cp /usr/share/pyshared/tvtk/tvtk_classes.zip dist/tvtk/ 


# testing

# run infobiotics-dashboard
dist/infobiotics-dashboard

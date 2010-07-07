#!/bin/bash

echo "freezing with py2app"
echo "additional flags (see 'python setup.py py2app --help') will by parsed to py2app"
echo

export ETS_TOOLKIT=qt4

PYTHON=/Library/Frameworks/Python.framework/Versions/Current/bin/python

# cleaning
#rm -rf build dist
bash ./clean.sh


# pre-freeze
chmod +x bin/infobiotics-dashboard.py


# freeze
easy_install pip
pip install py2app pexpect

${PYTHON} setup.py py2app $* &&
#--no-strip


# post-freeze

echo "creating qt.conf" &&
touch dist/InfobioticsDashboard.app/Contents/Resources/qt.conf &&

echo "unzipping tvtk_classes.zip in site-packages.zip" &&
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages &&
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages.zip &&
unzip -q dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip -d dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes &&
rm dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/site-packages/enthought/tvtk/tvtk_classes.zip &&

echo "copying libhdf5.6.dylib (could do this using 'py2app --frameworks'?)" &&
cp /Library/Frameworks/Python.framework/Versions/Current/lib/libhdf5.6.dylib dist/InfobioticsDashboard.app/Contents/MacOS/../Frameworks/libhdf5.6.dylib &&

# Tiger-specific
#install_name_tool -change "@rpath/libfreetype.6.dylib" "@loader_path/../../../../Frameworks/libfreetype.6.dylib" dist/Infobiotics\ Dashboard.app/Contents/Resources/lib/python2.6/matplotlib/ft2font.so

echo "patching matplotlib font_manager.py: http://www.mail-archive.com/matplotlib-users@lists.sourceforge.net/msg14295.html and https://trac.macports.org/ticket/22486"
patch dist/InfobioticsDashboard.app/Contents/Resources/lib/python2.6/matplotlib/font_manager.py <<HERE
Index: matplotlib/font_manager.py
===================================================================
--- matplotlib/font_manager.py	(revision 7951)
+++ matplotlib/font_manager.py	(working copy)
@@ -42,7 +42,7 @@
             see license/LICENSE_TTFQUERY.
 """
 
-import os, sys, glob
+import os, sys, glob, subprocess
 try:
     set
 except NameError:
@@ -292,16 +292,12 @@
     grab all of the fonts the user wants to be made available to
     applications, without needing knowing where all of them reside.
     """
-    try:
-        import commands
-    except ImportError:
-        return {}
-
     fontext = get_fontext_synonyms(fontext)
 
     fontfiles = {}
-    status, output = commands.getstatusoutput("fc-list file")
-    if status == 0:
+    pipe = subprocess.Popen(['fc-list', '', 'file'], stdout=subprocess.PIPE)
+    output = pipe.communicate()[0]
+    if pipe.returncode == 0:
         for line in output.split('\n'):
             fname = line.split(':')[0]
             if (os.path.splitext(fname)[1][1:] in fontext and
@@ -1244,11 +1240,11 @@
     import re
 
     def fc_match(pattern, fontext):
-        import commands
         fontexts = get_fontext_synonyms(fontext)
         ext = "." + fontext
-        status, output = commands.getstatusoutput('fc-match -sv "%s"' % pattern)
-        if status == 0:
+        pipe = subprocess.Popen(['fc-match', '-sv', pattern], stdout=subprocess.PIPE)
+        output = pipe.communicate()[0]
+        if pipe.returncode == 0:
             for match in _fc_match_regex.finditer(output):
                 file = match.group(1)
                 if os.path.splitext(file)[1][1:] in fontexts:

HERE


# testing

echo &&
echo "To run use:" &&
echo "dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard" &&
echo &&
echo "Running now" &&
dist/InfobioticsDashboard.app/Contents/MacOS/InfobioticsDashboard

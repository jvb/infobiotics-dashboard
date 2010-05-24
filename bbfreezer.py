#!/usr/bin/env python

import os, sys, distutils, glob, shutil

from bbfreeze import Freezer

f = Freezer(
    'dist',
    includes=[
        'vtk',
#        'enthought',
    ],
    excludes=[
        'Tkinter', 'Tkconstants', 'tcl', '_tkinter', 'numpy.f2py'
    ],
)
#f.addScript('bin/infobiotics-dashboard.pyw', gui_only=True)
f.addScript('bin/mcss.py', gui_only=False)
f()

## FIXME: I'm not sure how to install data files so that the image loading
## process will pick them up.  This doesn't work, I know that much:
#data_files = [
#    ("images", glob.glob("images/*.png")),
#    ]
#
#for subdir, files in data_files:
#    dest = "%s/%s" % (destdir, subdir)
#    if not os.path.exists(dest):
#        os.mkdir(dest)
#        print "Created %s" % dest
#    for file in files:
#        shutil.copy(file, "%s/%s" % (dest, os.path.basename(file)))
#        print "Copied %s" % file
        
'''
Item(
  # Item elements
  'tool2', 
  show_label=False,        
  style='readonly',
  editor = DNDEditor(
    # Editor elements
    image=ImageResource('exclusiveorgate_normal_normal.bmp', 
       search_path=['images']),# use search_path for bbfreeze
    ),
  ),
'''

#!/usr/bin/env python

# only needed for 'python setup.py py2app', 'py2app_imports.py' is not installed
import os.path
if os.path.exists('../py2app_imports.py'):
    from ..py2app_imports import *

import infobiotics.dashboard.run as run
run.main()

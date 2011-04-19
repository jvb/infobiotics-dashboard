#!/usr/bin/env python

# set process title
import setproctitle
setproctitle.setproctitle('Infobiotics Dashboard')

import infobiotics.dashboard.run as run
run.main()

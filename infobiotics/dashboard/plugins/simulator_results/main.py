# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: main.py 342 2009-09-09 11:49:07Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui/trunk/src/shared/main.py $
# $Author: jvb $
# $Revision: 342 $
# $Date: 2009-09-09 12:49:07 +0100 (Wed, 09 Sep 2009) $


'''
Setup and teardown of Infobiotics PyQt/Traits applications. 
'''


from PyQt4.QtGui import qApp, QApplication
import sys
import os
#from shared.settings import register_infobiotics_settings


EXIT_SUCCESS = 0


def begin(args=[]):
    sys.argv += args
    QApplication(sys.argv)
#    register_infobiotics_settings()
    return (qApp, sys.argv)


def begin_traits(args=[]):
#    os.environ['ETS_TOOLKIT'] = 'qt4' # must be before any Enthought imports in entry point 
    sys.argv += args
#    register_infobiotics_settings()
    return (qApp, sys.argv)


def end_with_qt_event_loop():
    return sys.exit(qApp.exec_())


def end(exit_code):
    return sys.exit(int(exit_code))



if __name__ == "__main__":
    begin()

    print "shared.main.__main__"

    end(EXIT_SUCCESS)

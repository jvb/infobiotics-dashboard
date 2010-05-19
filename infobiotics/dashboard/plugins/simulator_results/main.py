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

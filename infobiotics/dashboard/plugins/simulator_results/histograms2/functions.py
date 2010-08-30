# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


from PyQt4.QtGui import QApplication


def centreWindow(window):
    '''
    Centres a window on the current desktop.
    Should be called after the window has been shown.
    '''

    desktop = QApplication.desktop()
    rect = desktop.screenGeometry(window)
    x = (rect.width() / 2) - (window.width() / 2)
    y = (rect.height() / 2) - (window.height() / 2)
    window.setGeometry(x, y, window.width(), window.height())
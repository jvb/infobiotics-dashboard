from PyQt4.QtGui import QApplication

def centre_window(window):
    desktop = QApplication.desktop()
    rect = desktop.screenGeometry(window)
    x = (rect.width() / 2) - (window.width() / 2)
    y = (rect.height() / 2) - (window.height() / 2)
    window.setGeometry(x, y, window.width(), window.height())
    
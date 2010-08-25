from PyQt4.QtGui import QApplication

def centre_window(window):
    desktop = QApplication.desktop()
    rect = desktop.screenGeometry(window)
    x = (rect.width() / 2) - (window.width() / 2)
    y = (rect.height() / 2) - (window.height() / 2)
    window.setGeometry(x, y, window.width(), window.height())


from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import QUrl

def open_url(url):
    QDesktopServices.openUrl(QUrl(url, QUrl.TolerantMode))

def open_file(file):
    QDesktopServices.openUrl(QUrl('file://%s' % file, QUrl.TolerantMode))


import functools # http://docs.python.org/dev/library/functools.html#functools.wraps
from PyQt4.QtCore import Qt

def wait_cursor(f):
    ''' Change the mouse pointer to an hour glass for slow functions. '''
    @functools.wraps(f)
    def wrapper(self, *args, **kwds):
        self.setCursor(Qt.WaitCursor)
        result = f(self, *args, **kwds)
        self.setCursor(Qt.ArrowCursor)
        return result
    return wrapper


# http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg17328.html

from PyQt4.QtGui import QApplication, QClipboard
from PyQt4.QtCore import QEvent

def get_clipboard():
    if QApplication.instance() is None:
        raise ValueError("Can't return clipboard as application not instantiated.")
    cb = QApplication.clipboard()
    return cb

def validate_clipboard_mode(mode):
    if mode not in (QClipboard.Clipboard, QClipboard.Selection, QClipboard.FindBuffer):
        raise ValueError("Unrecognized mode: '%s', not in (QClipboard.Clipboard, QClipboard.Selection, QClipboard.FindBuffer)" % mode)

def clear_clipboard(mode=QClipboard.Clipboard):
    validate_clipboard_mode(mode)
    get_clipboard().clear(mode)

def copy_from_clipboard(function=QClipboard.text, mode=QClipboard.Clipboard):
    validate_clipboard_mode(mode)
    return function(get_clipboard(), mode)

def copy_text_from_clipbboard(mode=QClipboard.Clipboard):
    return copy_from_clipboard(QClipboard.text, mode)

def copy_to_clipboard(value, function=QClipboard.setText, clipboard=True, selection=True, find_buffer=True):
    cb = get_clipboard()
    if clipboard:
        function(cb, value, QClipboard.Clipboard)
    if selection and cb.supportsSelection():
        function(cb, value, QClipboard.Selection)
    if find_buffer and cb.supportsFindBuffer():
        function(cb, value, QClipboard.FindBuffer)
    event = QEvent(QEvent.Clipboard)
    QApplication.sendEvent(cb, event)

def copy_text_to_clipboard(text, clipboard=True, selection=True, find_buffer=True):
    copy_to_clipboard(text, QClipboard.setText, clipboard, selection, find_buffer)

#TODO repeat pattern for image, pixmap and mimeData


if __name__ == '__main__':
    def test_clipboard():
        app = QApplication([])
        copy_text_to_clipboard('text')
        print copy_text_from_clipbboard(), '.'
        clear_clipboard()
        print copy_text_from_clipbboard(), '.'
    test_clipboard()

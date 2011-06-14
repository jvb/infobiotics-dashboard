from PyQt4.QtGui import QApplication, qApp, QPushButton
from PyQt4.QtCore import QObject, SIGNAL
import subprocess
from win32con import STARTF_USESHOWWINDOW, SW_SHOWNOACTIVATE

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        QObject.connect(self, SIGNAL('clicked()'), self.go)
    def go(self):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= STARTF_USESHOWWINDOW
        si.wShowWindow = SW_SHOWNOACTIVATE
        subprocess.Popen(
            [
                'mcss', 
                'module1.params', 
                'runs=100', 
                'show_progress=true', 
                'progress_interval=1',
            ],
            cwd='d:\\home\\jvb\\My Dropbox\\workspace\\dashboard\\examples\\mcss\models', 
            startupinfo=si,
            creationflags=subprocess.CREATE_NEW_CONSOLE)
        
application = QApplication([])
button = Button('Go')
button.show()
qApp.exec_()

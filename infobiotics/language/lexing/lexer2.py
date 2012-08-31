# http://www.riverbankcomputing.com/pipermail/pyqt/2009-July/023709.html
import sys
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow, QColor, QFont
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom


if sys.hexversion < 0x020600F0:
     print('python 2.6 or greater is required by this program')
     sys.exit(1)

_sample = """
# Sample config file

this is a junk line

[FirstItem]
Width=100
Height=200
Colour=orange
Info=this is some
     multiline
     text

[SecondItem]
Width=200
Height=300
Colour=green
Info=
     this is some
     multiline
     text
"""


class MainWindow(QMainWindow):
     def __init__(self):
         QMainWindow.__init__(self)
         self.setWindowTitle('Custom Lexer For Config Files')
         self.setGeometry(50, 200, 400, 400)
         self.editor = QsciScintilla(self)
         self.editor.setUtf8(True)
         self.editor.setMarginWidth(2, 15)
         self.editor.setFolding(True)
         self.setCentralWidget(self.editor)
         self.lexer = ConfigLexer(self.editor)
         self.editor.setLexer(self.lexer)
         self.editor.setText(_sample)


class ConfigLexer(QsciLexerCustom):
     def __init__(self, parent):
         QsciLexerCustom.__init__(self, parent)
         self._styles = {
             0: 'Default',
             1: 'Comment',
             2: 'Section',
             3: 'Key',
             4: 'Assignment',
             5: 'Value',
             }
         for key,value in self._styles.iteritems():
             setattr(self, value, key)
         self._foldcompact = True

     def foldCompact(self):
         return self._foldcompact

     def setFoldCompact(self, enable):
         self._foldcompact = bool(enable)

     def language(self):
         return 'Config Files'

     def description(self, style):
         return self._styles.get(style, '')

     def defaultColor(self, style):
         if style == self.Default:
             return QColor('#000000')
         elif style == self.Comment:
             return QColor('#A0A0A0')
         elif style == self.Section:
             return QColor('#CC6600')
         elif style == self.Key:
             return QColor('#0000CC')
         elif style == self.Assignment:
             return QColor('#CC0000')
         elif style == self.Value:
             return QColor('#00CC00')
         return QsciLexerCustom.defaultColor(self, style)

     def defaultPaper(self, style):
         if style == self.Section:
             return QColor('#FFEECC')
         return QsciLexerCustom.defaultPaper(self, style)

     def defaultEolFill(self, style):
         if style == self.Section:
             return True
         return QsciLexerCustom.defaultEolFill(self, style)

     def defaultFont(self, style):
         if style == self.Comment:
             if sys.platform in ('win32', 'cygwin'):
                 return QFont('Comic Sans MS', 9)
             return QFont('Bitstream Vera Serif', 9)
         return QsciLexerCustom.defaultFont(self, style)

     def styleText(self, start, end):
         editor = self.editor()
         if editor is None:
             return

         SCI = editor.SendScintilla
         GETFOLDLEVEL = QsciScintilla.SCI_GETFOLDLEVEL
         SETFOLDLEVEL = QsciScintilla.SCI_SETFOLDLEVEL
         HEADERFLAG = QsciScintilla.SC_FOLDLEVELHEADERFLAG
         LEVELBASE = QsciScintilla.SC_FOLDLEVELBASE
         NUMBERMASK = QsciScintilla.SC_FOLDLEVELNUMBERMASK
         WHITEFLAG = QsciScintilla.SC_FOLDLEVELWHITEFLAG
         set_style = self.setStyling

         source = ''
         if end > editor.length():
             end = editor.length()
         if end > start:
             source = bytearray(end - start)
             SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
         if not source:
             return

         compact = self.foldCompact()

         index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)
         if index > 0:
             pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index - 1)
             state = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)
         else:
             state = self.Default

         self.startStyling(start, 0x1f)

         for line in source.splitlines(True):
             length = len(line)
             if length == 1:
                 whitespace = compact
                 state = self.Default
             else:
                 whitespace = False
                 firstchar = chr(line[0])
                 if firstchar in '#;':
                     state = self.Comment
                 elif firstchar == '[':
                     state = self.Section
                 elif firstchar in ' \t':
                     if state == self.Value or state == self.Assignment:
                         state = self.Value
                     else:
                         whitespace = compact and line.isspace()
                         state = self.Default
                 else:
                     pos = line.find('=')
                     if pos < 0:
                         pos = line.find(':')
                     else:
                         tmp = line.find(':', 0, pos)
                         if tmp >= 0:
                             pos = tmp
                     if pos > 0:
                         set_style(pos, self.Key)
                         set_style(1, self.Assignment)
                         length = length - pos - 1
                         state = self.Value
                     else:
                         state = self.Default
             set_style(length, state)

             if state == self.Section:
                 level = LEVELBASE | HEADERFLAG
             elif index > 0:
                 lastlevel = SCI(GETFOLDLEVEL, index - 1)
                 if lastlevel & HEADERFLAG:
                     level = LEVELBASE + 1
                 else:
                     level = lastlevel & NUMBERMASK
             else:
                 level = LEVELBASE

             if whitespace:
                 level |= WHITEFLAG
             if level != SCI(GETFOLDLEVEL, index):
                 SCI(SETFOLDLEVEL, index, level)

             index += 1

         if index > 0:
             lastlevel = SCI(GETFOLDLEVEL, index - 1)
             if lastlevel & HEADERFLAG:
                 level = LEVELBASE + 1
             else:
                 level = lastlevel & NUMBERMASK
         else:
             level = LEVELBASE

         lastlevel = SCI(GETFOLDLEVEL, index)
         SCI(SETFOLDLEVEL, index, level | lastlevel & ~NUMBERMASK)


if __name__ == "__main__":
     app = QApplication(sys.argv)
     app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
     win = MainWindow()
     win.show()
     sys.exit(app.exec_())
     
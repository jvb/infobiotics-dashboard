import sys
from PyQt4.QtCore import SIGNAL, SLOT, QString
from PyQt4.QtGui import QApplication, QMainWindow, QColor, QFont
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom

# The most important and hard part of this code was given by Baz WALTER on the PyQt list.

if sys.hexversion < 0x020600F0:
    print('python 2.6 or greater is required by this program')
    sys.exit(1)

_sample = """
This example shows how to highlight some specific lines or words.

+ A first level title bold and red
    + A secund level title bold and blue with a yellow background
Some text with green in green but also bold and underlined.
The digits are gray with an orange backround. You don't believe it, look at that : 1 , 2 , ... , 123456789...

It's very uggly but it shows how to do more pretty "highlighters".
"""


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Custom Lexer For Config Files')
        self.setGeometry(50, 200, 400, 400)
        self.editor = QsciScintilla(self)
        self.editor.setUtf8(True)

# LINES' NUMBER IN THE MARGIN
        self.editor.setMarginLineNumbers(1,True)
        self.editor.setMarginWidth(1, QString("-------"))
                # OK for 3 digits. This was found by direct tests...
# WRAPING
        self.editor.setWrapMode(True)

        self.setCentralWidget(self.editor)
        self.lexer = ConfigLexer(self.editor)
        self.editor.setLexer(self.lexer)
        self.editor.setText(_sample)


class ConfigLexer(QsciLexerCustom):
    def __init__(self, parent):
        QsciLexerCustom.__init__(self, parent)
        self._styles = { 
            0: 'Default',
            1: 'FirstLevelTitle',
            2: 'SecundLevelTitle',
            3: 'Green',
            4: 'Digits'
            }
        for key,value in self._styles.iteritems():
            setattr(self, value, key)

    def language(self):
        return 'Config Files'

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self, style):
        if style == self.Default:
            return QColor('#000000')
        elif style == self.FirstLevelTitle:
            return QColor('#FF0000')
        elif style == self.SecundLevelTitle:
            return QColor('#0000FF')
        elif style == self.Green:
            return QColor('#00FF00')
        elif style == self.Digits:
            return QColor('#AAAAAA')
        return QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
        font = QsciLexerCustom.defaultFont(self, style)

        if style == self.FirstLevelTitle or style == self.SecundLevelTitle:
            font.setBold(True)
        elif style == self.Green:
            font.setBold(True)
            font.setUnderline(True)
            
        return font

    def defaultPaper(self, style):
# Here we change the color of the background.
# We want to colorize all the background of the line.
# This is done by using the following method defaultEolFill() .
        if style == self.SecundLevelTitle:
            return QColor('#FFFF99')
        elif style == self.Digits:
            return QColor('#FFCC66')

        return QsciLexerCustom.defaultPaper(self, style)

    def defaultEolFill(self, style):
# This allowed to colorize all the background of a line.
        if style == self.SecundLevelTitle:
            return True
        return QsciLexerCustom.defaultEolFill(self, style)

    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        SCI = editor.SendScintilla
        set_style = self.setStyling

        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            source = bytearray(end - start)
            SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
        if not source:
            return

        self.startStyling(start, 0x1f)

        index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)
               
        for line in source.splitlines(True):
# Try to uncomment the following line to see in the console
# how Scintiallla works. You have to think in terms of isolated
# lines rather than globally on the whole text.
#            print line

            length = len(line)

            if line.startswith('+'):
                newState = self.FirstLevelTitle
            elif line.startswith('\t+') or line.startswith('    +'):
                newState = self.SecundLevelTitle
            else:
                pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                i = 0
                while i < length:
                    wordLength = 1

                    self.startStyling(i + pos, 0x1f)
                    if chr(line[i]) in '0123456789':
                        newState = self.Digits
                    else:
                        if line[i:].startswith('green'):
                            newState = self.Green
                            wordLength = len('green')
                        else:
                            newState = self.Default
                    i += wordLength
                    set_style(wordLength, newState)
                newState = None

            if newState:
                set_style(length, newState)

            index += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_()) 
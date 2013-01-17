import sys
from PyQt4.QtCore import SIGNAL, SLOT, QString
from PyQt4.QtGui import QApplication, QMainWindow, QColor, QFont
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import QsciScintillaBase as QsciBase

# Only QScintilla version 2.3+ has support for custom lexing
if Qsci.QSCINTILLA_VERSION < 0x20300:
    raise RuntimeError, "QScintilla version 2.3 or higher needed for CodeEditor"

from traits.api import Str, Unicode, List, Int, Event, Bool, TraitError, on_trait_change
from traits.trait_base import SequenceTypes

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the 
# traitsui.editors.code_editor file.
#from traitsui.editors.code_editor import ToolkitEditorFactory

from pyface.key_pressed_event import KeyPressedEvent
from pyface.ui.qt4.python_editor import _Scintilla

from traitsui.qt4.constants import OKColor, ErrorColor
from traitsui.qt4.editor import Editor
from traitsui.qt4.helper import pixmap_cache

from traitsui.qt4.code_editor import SourceLexer, SourceEditor, FindWidget

# Marker line constants:
MARK_MARKER = 0 # Marks a marked line
SEARCH_MARKER = 1 # Marks a line matching the current search
SELECTED_MARKER = 2 # Marks the currently selected line


class LPPLexer(SourceLexer):

    Default = 0

    MultiLinesComment_Start = 1
    MultiLinesComment = 2
    MultiLinesComment_End = 3
    SingleLineComment = 4
    __comment = (
        MultiLinesComment_Start,
        MultiLinesComment,
        MultiLinesComment_End,
        SingleLineComment,
    )

    Digits = 5

    SpatialDistribution_Start = 6
    SpatialDistribution = 7
    SpatialDistribution_End = 8
    _in_spatialDistribution = False

    positions = ''# 'start', 'inside', 'end'

    spatialDistribution = ''# 'start', 'inside', 'end'


    def __init__(self, editor):
        super(LPPLexer, self).__init__(editor)
        self._foldcompact = True

    def foldCompact(self):
        return self._foldcompact

    def setFoldCompact(self, enable):
        self._foldcompact = bool(enable)

    def language(self):
        return 'Lattice Population P systems'

    def description(self, style):
        return ''

    def defaultColor(self, style):
        if style == self.Default:
            return QColor('#000000')
        elif style in self.__comment:
            return QColor('#A0A0A0')
        return QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
#        if style in self.__comment:
#            if sys.platform in ('win32', 'cygwin'):
#                return QFont('Comic Sans MS', 9, QFont.Bold)
#            return QFont('Bitstream Vera Serif', 9, QFont.Bold)
#        return QsciLexerCustom.defaultFont(self, style)
        return QFont('Monospace', 10)

    def defaultPaper(self, style):
        # Here we change the color of the background.
        # We want to colorize all the background of the line.
        # This is done by using the following method defaultEolFill() .
        if style in self.__comment:
            return QColor('#FFEECC')
        return QsciLexerCustom.defaultPaper(self, style)

    def defaultEolFill(self, style):
        # This allowed to colorize all the background of a line.
        if style in self.__comment:
            return True
        return QsciLexerCustom.defaultEolFill(self, style)

    i = 1

    def styleText(self, start, end):
        super(LPPLexer, self).styleText(start, end)

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
#            source = bytearray(end - start)
            source = bytearray(end)
#            SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
            SCI(QsciScintilla.SCI_GETTEXTRANGE, 0, end, source)
        if not source:
            return
        print len(source), self.i
        self.i += 1

        compact = self.foldCompact()

#        index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)
        index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, 0)
        if index > 0:
            pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index - 1)
            prevState = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)
        else:
            prevState = self.Default

#        self.startStyling(start, 0x1f)
        self.startStyling(0, 0x1f)

        for line in source.splitlines(True):
            # Try to uncomment the following line to see in the console
            # how Scintiallla works. You have to think in terms of isolated
            # lines rather than globally on the whole text.
#            if '# Bacteria carrying' in line:
#                print self._in_spatialDistribution

            length = len(line)
            # We must take care of empty lines.
            # This is done here.
            if length == 1:
                if prevState == self.MultiLinesComment or prevState == self.MultiLinesComment_Start:
                    newState = self.MultiLinesComment
                else:
                    newState = self.Default
            # We work with a non empty line.
            else:

                # multi line comments
                if line.lstrip().startswith('/*'):
                    newState = self.MultiLinesComment_Start
                elif line.lstrip().startswith('*/'):
                    if prevState == self.MultiLinesComment or prevState == self.MultiLinesComment_Start:
                        newState = self.MultiLinesComment_End
                    else:
                        newState = self.Default

                # single line comments
                elif line.lstrip().startswith('#') and line.rstrip().endswith('#'):
                    if prevState == self.MultiLinesComment or prevState == self.MultiLinesComment_Start:
                        newState = self.MultiLinesComment
                    elif prevState == self.SpatialDistribution or prevState == self.SpatialDistribution_Start:
                        newState = self.SpatialDistribution
                    else:
                        newState = self.SingleLineComment

                # more multi line comments
                elif prevState == self.MultiLinesComment or prevState == self.MultiLinesComment_Start:
                    newState = self.MultiLinesComment

                # everything else
                else:
                    newState = self.Default


            set_style(length, newState)


            # folding

#            # Definition of the folding.
#            # Documentation : http://scintilla.sourceforge.net/ScintillaDoc.html#Folding
#            if newState == self.MultiLinesComment_Start:
#                if prevState == self.MultiLinesComment:
#                    level = LEVELBASE + 1
#                else:
#                    level = LEVELBASE | HEADERFLAG
#            elif newState == self.MultiLinesComment or newState == self.MultiLinesComment_End:
#                level = LEVELBASE + 1
#            else:
#                level = LEVELBASE

            # spatialDistribution
            # works:
            if line.lstrip().startswith('spatialDistribution'):
#                newState = self.SpatialDistribution_Start
#                self._in_spatialDistribution = True
                self.spatialDistribution = 'start'
            elif line.lstrip().startswith('endSpatialDistribution'):
#                self._in_spatialDistribution = False
                self.spatialDistribution = 'end'
            else:
                if self.spatialDistribution in ('start', 'inside'):
                    self.spatialDistribution == 'inside'
                else:
                    self.spatialDistribution == 'outside'
            #
#            if self._in_spatialDistribution:
            if self._in_spatialDistribution:
#                if newState == self.SpatialDistribution_Start:
                if self.spatialDistribution == 'start':
                    level = LEVELBASE | HEADERFLAG
                else:
                    level = LEVELBASE + 1
            else:
#                if newState == self.SpatialDistribution_End:
                if self.spatialDistribution = 'end':
                    level = LEVELBASE + 1
                else:
                    level = LEVELBASE
            # doesn't:
#            if line.lstrip().startswith('spatialDistribution'):
#                self.spatialDistribution = 'start'
#            elif line.lstrip().startswith('endSpatialDistribution'):
##                if self.spatialDistribution in ('start', 'inside'):
##                    self.spatialDistribution = 'end'
##                else:
##                    self.spatialDistribution = ''
#                self.spatialDistribution = 'end'
#            elif self.spatialDistribution in ('start', 'inside'):
#                self.spatialDistribution = 'inside'
#            else:
#                self.spatialDistribution = ''
##            print self.spatialDistribution
#            if self.spatialDistribution == 'start':
#                level = LEVELBASE + 1 | HEADERFLAG
#            elif self.spatialDistribution in ('inside', 'end'):
#                level = LEVELBASE + 1
#            else:
#                level = LEVELBASE

#            if line.lstrip().startswith('positions'):
#                self.positions = 'start'
#            elif line.lstrip().startswith('endPositions'):
#                if self.positions in ('start', 'inside'):
#                    self.positions = 'end'
#                else:
#                    self.positions = 'outside'
#            elif self.positions == 'start':
#                self.positions = 'inside'
#            elif self.positions == 'inside':
#                self.positions = 'inside'
#            elif self.positions == 'end':
#                self.positions = ''
#            else:
#                self.positions = ''
##            print self.positions
#            if self.positions == 'start':
#                level = LEVELBASE + 2 | HEADERFLAG
#            elif self.positions in ('inside', 'end'):
#                level = LEVELBASE + 2
#            else:
#                level = LEVELBASE

            SCI(SETFOLDLEVEL, index, level)

            pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index)
            prevState = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)

            index += 1
        pass

#class SourceEditor (Editor):
#    """ Editor for source code which uses the QScintilla widget.
#    """
#
#    #---------------------------------------------------------------------------
#    #  PyFace PythonEditor interface:
#    #---------------------------------------------------------------------------
#
#    # Event that is fired on keypresses:
#    key_pressed = Event(KeyPressedEvent)
#
#    #---------------------------------------------------------------------------
#    #  Editor interface:
#    #---------------------------------------------------------------------------
#
#    # The code editor is scrollable. This value overrides the default.
#    scrollable = True
#
#    #---------------------------------------------------------------------------
#    #  SoureEditor interface:
#    #---------------------------------------------------------------------------
#
#    # Is the editor read only?
#    readonly = Bool(False)
#
#    # The currently selected line
#    selected_line = Int
#
#    # The currently selected text
#    selected_text = Unicode
#
#    # The list of line numbers to mark
#    mark_lines = List(Int)
#
#    # The current line number
#    line = Event
#
#    # The current column
#    column = Event
#
#    # The Scintilla lexer to use
#    lexer = Int
#
#    # The lines to be dimmed
#    dim_lines = List(Int)
#    dim_color = Str
#    dim_style_number = Int(16) # 0-15 are reserved for the python lexer
#
#    # The lines to have squiggles drawn under them
#    squiggle_lines = List(Int)
#    squiggle_color = Str
#
#    #---------------------------------------------------------------------------
#    #  Finishes initializing the editor by creating the underlying toolkit
#    #  widget:
#    #---------------------------------------------------------------------------
#
#    def init (self, parent):
#        """ Finishes initializing the editor by creating the underlying toolkit
#            widget.
#        """
#        self.control = QtGui.QWidget()
#        layout = QtGui.QVBoxLayout(self.control)
#        layout.setMargin(0)
#
#        # Create the QScintilla widget
#        factory = self.factory
#        self._scintilla = control = _Scintilla(self, None)
#        layout.addWidget(control)
#
#        # Connect to the QScintilla signals that we care about
#        if not self.readonly:
#            QtCore.QObject.connect(control, QtCore.SIGNAL('lostFocus'),
#                                   self.update_object)
#            if factory.auto_set:
#                control.connect(control, QtCore.SIGNAL('textChanged()'),
#                                self.update_object)
#        if (factory.line != '') or (factory.column != ''):
#            # We need to monitor the line or column position being changed
#            control.connect(control,
#                    QtCore.SIGNAL('cursorPositionChanged(int, int)'),
#                    self._position_changed)
#
#        # Create the find bar
#        self._find_widget = FindWidget(self.find, self.control)
#        self._find_widget.hide()
#        layout.addWidget(self._find_widget)
#
#        # Make sure that the find bar will fit in the editor
#        min_width = self._find_widget.minimumSizeHint().width()
#        self.control.setMinimumWidth(min_width)
#
#        # Grab keyboard focus whenever the find bar is closed
#        QtCore.QObject.connect(self._find_widget, QtCore.SIGNAL('hidden()'),
#                               self._scintilla, QtCore.SLOT('setFocus()'))
#
#        # Set up the lexer. Before we set our custom lexer, we call setLexer
#        # with the QSciLexer that will set the keywords and styles for the
#        # basic syntax lexing. We save and then restore these keywords/styles 
#        # because they get nuked when we call setLexer again.
#        self.lexer = getattr(QsciBase, 'SCLEX_' + self.factory.lexer.upper(),
#                             QsciBase.SCLEX_NULL)
#        base_lexer_class = LEXER_MAP.get(self.lexer)
#        if base_lexer_class:
#            lexer = base_lexer_class(control)
#            control.setLexer(lexer)
#            keywords = lexer.keywords(1)
#            styles = []
#            attr_names = ['FORE', 'BACK', 'BOLD', 'ITALIC', 'SIZE', 'UNDERLINE']
#            for style in xrange(128):
#                attrs = [ control.SendScintilla(getattr(QsciBase, 'SCI_STYLEGET' + a), style)
#                          for a in attr_names ]
#                styles.append(attrs)
#        lexer = SourceLexer(self)
#        control.setLexer(lexer)
#        if base_lexer_class:
#            if keywords:
#                control.SendScintilla(QsciBase.SCI_SETKEYWORDS, 0, keywords)
#            for style, attrs in enumerate(styles):
#                for attr_num, attr in enumerate(attrs):
#                    msg = getattr(QsciBase, 'SCI_STYLESET' + attr_names[attr_num])
#                    control.SendScintilla(msg, style, attr)
#
#        # Set a monspaced font. Use the (supposedly) same font and size as the
#        # wx version.
#        for style in xrange(128):
#            f = lexer.font(style)
#            f.setFamily('courier new')
#            f.setPointSize(10)
#            lexer.setFont(f, style)
#
#        # Mark the maximum line size.
#        control.setEdgeMode(Qsci.QsciScintilla.EdgeLine)
#        control.setEdgeColumn(79)
#
#        # Display line numbers in the margin.
#        if factory.show_line_numbers:
#            control.setMarginLineNumbers(1, True)
#            control.setMarginWidth(1, 45)
#        else:
#            control.setMarginWidth(1, 4)
#            control.setMarginsBackgroundColor(QtCore.Qt.white)
#
#        # Configure indentation and tabs.
#        control.setIndentationsUseTabs(False)
#        control.setTabWidth(4)
#
#        # Configure miscellaneous control settings:
#        control.setEolMode(Qsci.QsciScintilla.EolUnix)
#
#        if self.readonly:
#            control.setReadOnly(True)
#
#        # Define the markers we use:
#        control.markerDefine(Qsci.QsciScintilla.Background, MARK_MARKER)
#        control.setMarkerBackgroundColor(factory.mark_color_, MARK_MARKER)
#
#        control.markerDefine(Qsci.QsciScintilla.Background, SEARCH_MARKER)
#        control.setMarkerBackgroundColor(factory.search_color_, SEARCH_MARKER)
#
#        control.markerDefine(Qsci.QsciScintilla.Background, SELECTED_MARKER)
#        control.setMarkerBackgroundColor(factory.selected_color_, SELECTED_MARKER)
#
#        # Make sure the editor has been initialized:
#        self.update_editor()
#
#        # Set up any event listeners:
#        self.sync_value(factory.mark_lines, 'mark_lines', 'from',
#                         is_list=True)
#        self.sync_value(factory.selected_line, 'selected_line', 'from')
#        self.sync_value(factory.selected_text, 'selected_text', 'to')
#        self.sync_value(factory.line, 'line')
#        self.sync_value(factory.column, 'column')
#
#        self.sync_value(factory.dim_lines, 'dim_lines', 'from', is_list=True)
#        if self.factory.dim_color == '':
#            self.dim_color = 'grey'
#        else:
#            self.sync_value(factory.dim_color, 'dim_color', 'from')
#
#        self.sync_value(factory.squiggle_lines, 'squiggle_lines', 'from',
#                        is_list=True)
#        if factory.squiggle_color == '':
#            self.squiggle_color = 'red'
#        else:
#            self.sync_value(factory.squiggle_color, 'squiggle_color', 'from')
#
#        # Set the control tooltip:
#        self.set_tooltip()
#
#    #---------------------------------------------------------------------------
#    #  Disposes of the contents of an editor:    
#    #---------------------------------------------------------------------------
#
#    def dispose (self):
#        """ Disposes of the contents of an editor.
#        """
#        # Make sure that the editor does not try to update as the control is
#        # being destroyed:
#        QtCore.QObject.disconnect(self._scintilla, QtCore.SIGNAL('lostFocus'),
#                                  self.update_object)
#
#        super(SourceEditor, self).dispose()
#
#    #---------------------------------------------------------------------------
#    #  Handles the user entering input data in the edit control:
#    #---------------------------------------------------------------------------
#
#    def update_object (self):
#        """ Handles the user entering input data in the edit control.
#        """
#        if not self._locked:
#            try:
#                value = unicode(self._scintilla.text())
#                if isinstance(self.value, SequenceTypes):
#                    value = value.split()
#                self.value = value
#                self._scintilla.lexer().setPaper(OKColor)
#            except TraitError, excp:
#                pass
#
#    #---------------------------------------------------------------------------
#    #  Updates the editor when the object trait changes external to the editor:
#    #---------------------------------------------------------------------------
#
#    def update_editor (self):
#        """ Updates the editor when the object trait changes externally to the 
#            editor.
#        """
#        self._locked = True
#        new_value = self.value
#        if isinstance(new_value, SequenceTypes):
#            new_value = '\n'.join([ line.rstrip() for line in new_value ])
#        control = self._scintilla
#        if control.text() != new_value:
#            readonly = control.isReadOnly()
#            control.setReadOnly(False)
#            vsb = control.verticalScrollBar()
#            l1 = vsb.value()
#            line, column = control.getCursorPosition()
#            control.setText(new_value)
#            control.setCursorPosition(line, column)
#            vsb.setValue(l1)
#            control.setReadOnly(readonly)
#            self._mark_lines_changed()
#            if self.factory.selected_line:
#                self._selected_line_changed()
#        self._locked = False
#
#    #---------------------------------------------------------------------------
#    #  Handles an error that occurs while setting the object's trait value:
#    #---------------------------------------------------------------------------
#
#    def error (self, excp):
#        """ Handles an error that occurs while setting the object's trait value.
#        """
#        self._scintilla.lexer().setPaper(ErrorColor)
#
#    #---------------------------------------------------------------------------
#    #  Finds and selects the next or previous match of text:
#    #---------------------------------------------------------------------------
#
#    def find (self, text, forward, match_case):
#        """ Finds and selects the next or previous match of text.
#        """
#        line, index = self._scintilla.getCursorPosition()
#        if not forward:
#            index -= len(self._scintilla.selectedText())
#
#        # Arguments: expr, is regex, case_sensitive, whole words only, wrap
#        #            around, is forward, line, index in line
#        self._scintilla.findFirst(text, False, match_case, False, True, forward,
#                                  line, index)
#
#    #-- UI preference save/restore interface -----------------------------------
#
#    #---------------------------------------------------------------------------
#    #  Restores any saved user preference information associated with the 
#    #  editor:
#    #---------------------------------------------------------------------------
#
#    def restore_prefs (self, prefs):
#        """ Restores any saved user preference information associated with the 
#            editor.
#        """
#        if self.factory.key_bindings is not None:
#            key_bindings = prefs.get('key_bindings')
#            if key_bindings is not None:
#                self.factory.key_bindings.merge(key_bindings)
#
#    #---------------------------------------------------------------------------
#    #  Returns any user preference information associated with the editor:
#    #---------------------------------------------------------------------------
#
#    def save_prefs (self):
#        """ Returns any user preference information associated with the editor.
#        """
#        return { 'key_bindings': self.factory.key_bindings }
#
#    #---------------------------------------------------------------------------
#    #  Handles the set of 'marked lines' being changed:  
#    #---------------------------------------------------------------------------
#
#    def _mark_lines_changed (self):
#        """ Handles the set of marked lines being changed.
#        """
#        lines = self.mark_lines
#        control = self._scintilla
#        lc = control.lines()
#        control.markerDeleteAll(MARK_MARKER)
#        for line in lines:
#            if 0 < line <= lc:
#                control.markerAdd(line - 1, MARK_MARKER)
#
#    def _mark_lines_items_changed (self):
#        self._mark_lines_changed()
#
#    #---------------------------------------------------------------------------
#    #  Handles the currently 'selected line' being changed:  
#    #---------------------------------------------------------------------------
#
#    def _selected_line_changed (self):
#        """ Handles a change in which line is currently selected.
#        """
#        line = self.selected_line
#        control = self._scintilla
#        line = max(1, min(control.lines(), line)) - 1
#        control.markerDeleteAll(SELECTED_MARKER)
#        control.markerAdd(line, SELECTED_MARKER)
#        _, column = control.getCursorPosition()
#        control.setCursorPosition(line, column)
#        if self.factory.auto_scroll:
#            control.ensureLineVisible(line)
#
#    #---------------------------------------------------------------------------
#    #  Handles the 'line' trait being changed:  
#    #---------------------------------------------------------------------------
#
#    def _line_changed (self, line):
#        if not self._locked:
#            control = self._scintilla
#            _, column = control.getCursorPosition()
#            self._scintilla.setCursorPosition(line - 1, column)
#
#    #---------------------------------------------------------------------------
#    #  Handles the 'column' trait being changed:  
#    #---------------------------------------------------------------------------
#
#    def _column_changed (self, column):
#        if not self._locked:
#            control = self._scintilla
#            line, _ = control.getCursorPosition()
#            self._scintilla.setCursorPosition(line, column - 1)
#
#    #---------------------------------------------------------------------------
#    #  Handles the cursor position being changed:  
#    #---------------------------------------------------------------------------
#
#    def _position_changed(self, line, column):
#        """ Handles the cursor position being changed.
#        """
#        control = self._scintilla
#        self._locked = True
#        self.line = line
#        self.column = column
#        self._locked = False
#        self.selected_text = unicode(control.selectedText())
#
#    #---------------------------------------------------------------------------
#    #  Handles a key being pressed within the editor:    
#    #---------------------------------------------------------------------------
#
#    def _key_pressed_changed (self, event):
#        """ Handles a key being pressed within the editor.
#        """
#        key_bindings = self.factory.key_bindings
#        if key_bindings:
#            processed = key_bindings.do(event.event, self.ui.handler,
#                                        self.ui.info)
#        else:
#            processed = False
#        if not processed and event.event.matches(QtGui.QKeySequence.Find):
#            self._find_widget.show()
#
#    #---------------------------------------------------------------------------
#    #  Handles the styling of the editor:
#    #---------------------------------------------------------------------------
#
#    def _dim_color_changed(self):
#        self._scintilla.SendScintilla(QsciBase.SCI_STYLESETFORE,
#                                      self.dim_style_number,
#                                      QtGui.QColor(self.dim_color))
#
#    def _squiggle_color_changed(self):
#        self._scintilla.SendScintilla(QsciBase.SCI_INDICSETSTYLE, 2,
#                                      QsciBase.INDIC_SQUIGGLE)
#        self._scintilla.SendScintilla(QsciBase.SCI_INDICSETFORE, 2,
#                                      QtGui.QColor(self.squiggle_color))
#
#    @on_trait_change('dim_lines, squiggle_lines')
#    def _style_document(self):
#        self._scintilla.recolor()


from traits.api import Int
from PyQt4 import QtGui

class _LPPEditor(SourceEditor):

    def init (self, parent):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        self.control = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(self.control)
        layout.setMargin(0)

        # Create the QScintilla widget
        factory = self.factory
        self._scintilla = control = _Scintilla(self, None)
        layout.addWidget(control)

        # Connect to the QScintilla signals that we care about
        if not self.readonly:
            QtCore.QObject.connect(control, QtCore.SIGNAL('lostFocus'),
                                   self.update_object)
            if factory.auto_set:
                control.connect(control, QtCore.SIGNAL('textChanged()'),
                                self.update_object)
        if (factory.line != '') or (factory.column != ''):
            # We need to monitor the line or column position being changed
            control.connect(control,
                    QtCore.SIGNAL('cursorPositionChanged(int, int)'),
                    self._position_changed)

        # Create the find bar
        self._find_widget = FindWidget(self.find, self.control)
        self._find_widget.hide()
        layout.addWidget(self._find_widget)

        # Make sure that the find bar will fit in the editor
        min_width = self._find_widget.minimumSizeHint().width()
        self.control.setMinimumWidth(min_width)

        # Grab keyboard focus whenever the find bar is closed
        QtCore.QObject.connect(self._find_widget, QtCore.SIGNAL('hidden()'),
                               self._scintilla, QtCore.SLOT('setFocus()'))

#        # Set up the lexer. Before we set our custom lexer, we call setLexer
#        # with the QSciLexer that will set the keywords and styles for the
#        # basic syntax lexing. We save and then restore these keywords/styles 
#        # because they get nuked when we call setLexer again.
#        self.lexer = getattr(QsciBase, 'SCLEX_' + self.factory.lexer.upper(),
#                             QsciBase.SCLEX_NULL)
#        base_lexer_class = LEXER_MAP.get(self.lexer)
#        if base_lexer_class:
#            lexer = base_lexer_class(control)
#            control.setLexer(lexer)
#
#            # commenting these removes squiggle_lines, etc. but styles work 
#            keywords = lexer.keywords(1)
#            styles = []
#            attr_names = ['FORE', 'BACK', 'BOLD', 'ITALIC', 'SIZE', 'UNDERLINE']
#            for style in xrange(128):
#                attrs = [ control.SendScintilla(getattr(QsciBase, 'SCI_STYLEGET' + a), style)
#                          for a in attr_names ]
#                styles.append(attrs)
#        lexer = SourceLexer(self)
#        control.setLexer(lexer)
#        if base_lexer_class:
#            if keywords:
#                control.SendScintilla(QsciBase.SCI_SETKEYWORDS, 0, keywords)
#            for style, attrs in enumerate(styles):
#                for attr_num, attr in enumerate(attrs):
#                    msg = getattr(QsciBase, 'SCI_STYLESET' + attr_names[attr_num])
#                    control.SendScintilla(msg, style, attr)

        self.lexer = 2
        lexer = LPPLexer(self)
        control.setLexer(lexer)

#        # Set a monspaced font. Use the (supposedly) same font and size as the #TODO
#        # wx version.
#        for style in xrange(128):
#            f = lexer.font(style)
#            f.setFamily('courier new')
#            f.setPointSize(10)
#            lexer.setFont(f, style)

        # Mark the maximum line size.
        control.setEdgeMode(Qsci.QsciScintilla.EdgeLine)
        control.setEdgeColumn(79)

        # Display line numbers in the margin.
        if factory.show_line_numbers:
            control.setMarginLineNumbers(1, True)
            control.setMarginWidth(1, 45)
        else:
            control.setMarginWidth(1, 4)
            control.setMarginsBackgroundColor(QtCore.Qt.white)

        # Configure indentation and tabs.
        control.setIndentationsUseTabs(False)
        control.setTabWidth(4)

        # Configure miscellaneous control settings:
        control.setEolMode(Qsci.QsciScintilla.EolUnix)

        if self.readonly:
            control.setReadOnly(True)

        # Define the markers we use:
        control.markerDefine(Qsci.QsciScintilla.Background, MARK_MARKER)
        control.setMarkerBackgroundColor(factory.mark_color_, MARK_MARKER)

        control.markerDefine(Qsci.QsciScintilla.Background, SEARCH_MARKER)
        control.setMarkerBackgroundColor(factory.search_color_, SEARCH_MARKER)

        control.markerDefine(Qsci.QsciScintilla.Background, SELECTED_MARKER)
        control.setMarkerBackgroundColor(factory.selected_color_, SELECTED_MARKER)

#        control.setUtf8(True)
        if factory.foldable:
            control.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle) # + OR - TO FOLD OR UNFOLD

        # Make sure the editor has been initialized:
        self.update_editor()

        # Set up any event listeners:
        self.sync_value(factory.mark_lines, 'mark_lines', 'from', is_list=True)
        self.sync_value(factory.selected_line, 'selected_line', 'from')
        self.sync_value(factory.selected_text, 'selected_text', 'to')
        self.sync_value(factory.line, 'line')
        self.sync_value(factory.column, 'column')

        self.sync_value(factory.dim_lines, 'dim_lines', 'from', is_list=True)
        if self.factory.dim_color == '':
            self.dim_color = 'grey'
        else:
            self.sync_value(factory.dim_color, 'dim_color', 'from')

        self.sync_value(factory.squiggle_lines, 'squiggle_lines', 'from', is_list=True)
        if factory.squiggle_color == '':
            self.squiggle_color = 'red'
        else:
            self.sync_value(factory.squiggle_color, 'squiggle_color', 'from')

        # Set the control tooltip:
        self.set_tooltip()


from traitsui.api import BasicEditorFactory
from traits.api import Str, Color, Enum, Bool, Instance
from infobiotics.commons.traits_.ui.key_bindings import KeyBindings

class LPPEditor(BasicEditorFactory):
    klass = _LPPEditor

    # Object trait containing list of line numbers to mark (optional)
    mark_lines = Str

    # Background color for marking lines
    mark_color = Color(0xECE9D8)

    # Object trait containing the currently selected line (optional)
    selected_line = Str

    # Object trait containing the currently selected text (optional)
    selected_text = Str

    # Background color for selected lines
    selected_color = Color(0xA4FFFF)

    # Where should the search toolbar be placed?
    search = Enum('top', 'bottom', 'none')

    # Background color for lines that match the current search
    search_color = Color(0xFFFF94)

    # Current line
    line = Str

    # Current column
    column = Str

    # Should code folding be enabled?
    foldable = Bool(True)

    # Should line numbers be displayed in the margin?
    show_line_numbers = Bool(True)

    # Is user input set on every change?
    auto_set = Bool(True)

    # Should the editor auto-scroll when a new **selected_line** value is set?
    auto_scroll = Bool(True)

    # Optional key bindings associated with the editor    
    key_bindings = Instance(KeyBindings)# 'traitsui.key_bindings.KeyBindings' ) #TODO

    # Calltip clicked event
    calltip_clicked = Str

    # The lexer to use. Default is 'python'; 'null' indicates no lexing.
    lexer = Str('python') #TODO

    # Object trait containing the list of line numbers to dim (optional)
    dim_lines = Str

    # Object trait to dim lines to. Can be of form #rrggbb or a color spec. If
    # not specified, dark grey is used.
    dim_color = Str

    # Object trait containing the list of line numbers to put squiggles under
    # (optional)
    squiggle_lines = Str

    # Object trait for the color of squiggles. If not specified, red is used.
    squiggle_color = Str


test = """
# Author: Francisco J. Romero-Campero                                      #
# Date: July 2010                                                           #
# Description: A multicelluar system consisting of a bacterial colony   #
#              combining bacteria carrying the same gene under three different #
#                    regulatory mechanisms. Namely, unregulated expression, positive #
#                     autoregulation and negative autoregulation #

LPPsystem negativeAutoregulationModel

    # Cell types specified as individual SP systems #
    SPsystems
        SPsystem UnReg from UnReg.sps
          SPsystem PAR from PAR.sps
        SPsystem NAR from NAR.sps
    endSPsystems

    # The geometry of the system is determine using a regular finite point lattice #
    lattice rectangular from rectangular.lat

    # Special distribution of the cells over the lattice #
    spatialDistribution
        
        # Bacteria carrying gene1 expressed constitutively are place on the leftmost part #
          # of the bacterial colony #
        positions for UnReg

            parameters
                parameter i = 0:1:9
                parameter j = 0:1:9
            endParameters
            
            coordinates
                x = i
                y = j
            endCoordinates

        endPositions


        # Bacteria carrying gene1 regulating itself positively are place on the rightmost part #
          # of the bacterial colony #
        positions for PAR

            parameters
                parameter i = 15:1:24
                parameter j = 0:1:10
            endParameters
            
            coordinates
                x = i
                y = j
            endCoordinates

        endPositions


        # Bacteria carrying gene1 regulating itself negatively are place on the rightmost part #
          # of the bacterial colony #
        positions for NAR

            parameters
                parameter i = 30:1:39
                parameter j = 0:1:10
            endParameters
            
            coordinates
                x = i
                y = j
            endCoordinates

        endPositions

    endSpatialDistribution

endLPPsystem

"""

from traits.api import HasTraits, Str, List, Int
from traitsui.api import View, Item
class Test(HasTraits):
    model = Str(test)
    squiggle_lines = List(Int, [10, 13])
    mark_lines = List(Int, [1, 7])
    dim_lines = List(Int, [9, 13])

    view = View(
        Item('model',
            show_label=False,
            style='custom', #TODO BasicEditorFactory?
            editor=LPPEditor(
                squiggle_lines='squiggle_lines',
                mark_lines='mark_lines',
                dim_lines='dim_lines',
            ),
        ),
        width=640,
        height=480,
        resizable=True,
    )


if __name__ == '__main__':
    Test().configure_traits()

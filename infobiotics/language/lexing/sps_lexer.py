import sys
from PyQt4.QtCore import SIGNAL, SLOT, QString
from PyQt4.QtGui import QApplication, QMainWindow, QColor, QFont
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom

# The most important and hard part of this code was given by Baz WALTER on the PyQt list.

if sys.hexversion < 0x020600F0:
    print('python 2.6 or greater is required by this program')
    sys.exit(1)

#_sample = """
#/* This example uses
#this multi-line coment
#which can be extanded or retracted.
#
#The end must be the following line.
#*/
#
#A text outside a MultiLinesComment
#is not retactable.
#
#
#/* Another
#
#test.
#*/
#"""
_sample = '''
SPsystem senderCell

    alphabet
        Pconst_geneLuxI 
        proteinLuxI
        proteinLuxI_Rib
        rnaLuxI
        rnaLuxI_RNAP
        signal3OC12
    endAlphabet

    compartments
        cell
    endCompartments

    initialMultisets
        initialMultiset cell
            Pconst_geneLuxI 1
        endInitialMultiset
    endInitialMultisets

    ruleSets

        ruleSet cell

            Pconst({LuxI},{0.001},{cell}) from library.plb

            PostTransc({LuxI},{3.36,0.0667,0.004,3.78,0.0667},{cell}) from library.plb

            r1: [ proteinLuxI ]_cell -c1-> [ proteinLuxI + signal3OC12 ]_cell                        c1 = 1

          r2: [ signal3OC12 ]_cell =(1,0)=[ ] -c2-> [ ]_cell =(1,0)=[ signal3OC12 ]            c2 = 2
          r3: [ signal3OC12 ]_cell =(-1,0)=[ ] -c3-> [ ]_cell =(-1,0)=[ signal3OC12 ]        c3 = 2
          r4: [ signal3OC12 ]_cell =(0,1)=[ ] -c2-> [ ]_cell =(0,1)=[ signal3OC12 ]            c4 = 2
          r5: [ signal3OC12 ]_cell =(0,-1)=[ ] -c2-> [ ]_cell =(0,-1)=[ signal3OC12 ]        c5 = 2



        endRuleSet

    endRuleSets

endSPsystem


SPsystem pulsingCell

    alphabet
        CI2
        LuxR2
        Pconst_geneLuxR
        PluxPR_CI2_geneGFP
        PluxPR_LuxR2_CI2_geneGFP
        PluxPR_LuxR2_geneGFP
        PluxPR_geneGFP
        Plux_LuxR2_geneCI
        Plux_LuxR2_geneLuxI
        Plux_geneCI
        Plux_geneLuxI
        proteinCI
        proteinCI_Rib
        proteinGFP
        proteinGFP_Rib
        proteinLuxI
        proteinLuxI_Rib
        proteinLuxR
        proteinLuxR_3OC12
        proteinLuxR_Rib
        rnaCI
        rnaCI_RNAP
        rnaGFP
        rnaGFP_RNAP
        rnaLuxI
        rnaLuxI_RNAP
        rnaLuxR
        rnaLuxR_RNAP
        signal3OC12
    endAlphabet

   compartments
      bacterium
   endCompartments

   initialMultisets
       initialMultiset bacterium
         Pconst_geneLuxR 1
         Plux_geneCI 1
            Plux_geneLuxI 1
         PluxPR_geneGFP 1
      endInitialMultiset
    endInitialMultisets

   ruleSets

       ruleSet bacterium

            Pconst({LuxR},{0.1},{bacterium}) from library.plb
            PostTransc({LuxR},{3.2,0.3,0.04,3.6,0.075},{bacterium}) from library.plb    
            DimSig({LuxR,3OC12,LuxR2},{1,0.0154,1,0.0154},{bacterium}) from library.plb

            Plux({CI},{1,1,4},{bacterium}) from library.plb
            PostTransc({CI},{3.2,0.02,0.04,3.6,0.1},{bacterium}) from library.plb
            Dim({CI,CI2},{1,0.00554},{bacterium}) from library.plb

            Plux({LuxI},{1,1,4},{bacterium}) from library.plb
            PostTransc({LuxI},{3.36,0.0667,0.004,3.78,0.0667},{cell}) from library.plb


            PluxPR({GFP},{1,1,1,1,5,0.0000001,5,0.0000001,4},{bacterium}) from library.plb
            PostTransc({GFP},{3.36,0.667,0.04,3.78,0.0667},{bacterium}) from library.plb

         Diffusion({3OC12},{0.1},{bacterium}) from library.plb

      endRuleSet

   endRuleSets

endSPsystem


# Author: Francisco J. Romero-Campero                                         #
# Date: 14 May 2010                                                                  #
# Description: A model of three genes forming an incoherent feed    #
#                    forward loop                                                    #

SPsystem negativeAutoregulation

    # Molecular species in the system # 
    alphabet
        gene1
        gene2
        gene3
        protein1
        protein1_gene2
        protein1_gene3
        protein2
        protein2_gene3
        protein3
        rna1
        rna2
        rna3
    endAlphabet

    # The system consists of a single compartment #
   compartments
        bacterium
   endCompartments
      
    # Initial number of molecules present in the system #
   initialMultisets
     initialMultiset bacterium
       gene1     1
         gene2    1
         gene3    1
     endInitialMultiset
   endInitialMultisets

    # Rules describing the molecular interactions in the system #    
      ruleSets
        
        ruleSet bacterium    

            # Constitutive expression of gene 1 #
            UnReg({1},{0.025},{bacterium}) from basicLibrary.plb
            PostTransc({1},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

            # Positive regulation of gene 1 over gene 2 #
            PosReg({1,2},{0.1,0.1,0.025},{bacterium}) from basicLibrary.plb
            PostTransc({2},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

            # Positive regulation of gene 1 over gene 3 #
            PosReg({1,3},{1,1,0.25},{bacterium}) from basicLibrary.plb
            PostTransc({3},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

            # Negative regulation of gene 2 over gene 3 #
            NegReg({2,3},{1,0.001},{bacterium}) from basicLibrary.plb

        endRuleSet

    endRuleSets 

endSPsystem



'''






class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Custom lexer for stochastic P system (.sps) files')
        self.setGeometry(50, 200, 400, 400)
        self.editor = QsciScintilla(self)
        self.editor.setUtf8(True)

# + OR - TO FOLD OR UNFOLD
        self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
# LINES' NUMBER IN THE MARGIN
        self.editor.setMarginLineNumbers(1,True)
        self.editor.setMarginWidth(1, QString("-------"))
                # OK for 3 digits. This was found by direct tests...

        self.setCentralWidget(self.editor)
        self.lexer = ConfigLexer(self.editor)
        self.editor.setLexer(self.lexer)
        self.editor.setText(_sample)


class ConfigLexer(QsciLexerCustom):
    def __init__(self, parent):
        QsciLexerCustom.__init__(self, parent)
        self._styles = {
            0: 'Default',
            1: 'MultiLinesComment_Start',
            2: 'MultiLinesComment',
            3: 'MultiLinesComment_End',
            4: 'SingleLineComment'
            }
        
        '''TODO
SPsystem endSPsystem
alphabet endAlphabet
compartments endCompartments
initialMultisets endInitialMultisets
initialMultiset endInitialMultiset
ruleSets endRuleSets
ruleSet endRuleSet
        '''

        for key,value in self._styles.iteritems():
            setattr(self, value, key)
        self._foldcompact = True
        self.__comment = [self.MultiLinesComment,
                          self.MultiLinesComment_End,
                          self.MultiLinesComment_Start,
                          self.SingleLineComment]

    def foldCompact(self):
        return self._foldcompact

    def setFoldCompact(self, enable):
        self._foldcompact = bool(enable)

    def language(self):
        return 'stochastic P system'

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self, style):
        if style == self.Default:
            return QColor('#000000')
        elif style in self.__comment:
            return QColor('#A0A0A0')
        return QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
        if style in self.__comment:
            if sys.platform in ('win32', 'cygwin'):
                return QFont('Comic Sans MS', 9, QFont.Bold)
            return QFont('Bitstream Vera Serif', 9, QFont.Bold)
        return QsciLexerCustom.defaultFont(self, style)

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
            prevState = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)
        else:
            prevState = self.Default

        self.startStyling(start, 0x1f)

        for line in source.splitlines(True):
# Try to uncomment the following line to see in the console
# how Scintiallla works. You have to think in terms of isolated
# lines rather than globally on the whole text.
#            print line

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
                if line.startswith('/*'):
                    newState = self.MultiLinesComment_Start
                elif line.startswith('*/'):
                    if prevState == self.MultiLinesComment or prevState == self.MultiLinesComment_Start:
                        newState = self.MultiLinesComment_End
                    else:
                        newState = self.Default
                elif line.startswith('//'):
                    if prevState == self.MultiLinesComment or prevState == self.MultiLinesComment_Start:
                        newState = self.MultiLinesComment
                    else:
                        newState = self.SingleLineComment
                elif prevState == self.MultiLinesComment or prevState == self.MultiLinesComment_Start:
                    newState = self.MultiLinesComment
                else:              
                    newState = self.Default

            set_style(length, newState)

# Definition of the folding.
# Documentation : http://scintilla.sourceforge.net/ScintillaDoc.html#Folding
            if newState == self.MultiLinesComment_Start:
                if prevState == self.MultiLinesComment:
                    level = LEVELBASE + 1
                else:
                    level = LEVELBASE | HEADERFLAG
            elif newState == self.MultiLinesComment or newState == self.MultiLinesComment_End:
                level = LEVELBASE + 1
            else:
                level = LEVELBASE

            SCI(SETFOLDLEVEL, index, level)

            pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index)
            prevState = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)

            index += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_()) 
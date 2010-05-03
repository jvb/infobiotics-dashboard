from bnf_editor import BNFEditor


class SPSEditor(BNFEditor):

#    key_bindings = Instance(KeyBindings) # The key bindings used by the editor
    wildcard = 'Stochastic P system specification (*.sps)'
    untitled_prefix='P system '    
    text = '''SPsystem repressilator
 
    alphabet
     geneCI
     geneLacI
     geneTetR
     proteinCI
     proteinCI2_geneLacI
     proteinCI_geneLacI
     proteinLacI
     proteinLacI2_geneTetR
     proteinLacI_geneTetR
     proteinTetR
     proteinTetR2_geneCI
     proteinTetR_geneCI
     rnaCI
     rnaLacI
     rnaTetR
    endAlphabet

   compartments
        bacterium
   endCompartments
      
   initialMultisets
     initialMultiset bacterium
       geneLacI 1
       geneCI 1
       geneTetR 1
     endInitialMultiset
   endInitialMultisets

      ruleSets
        
        ruleSet bacterium    

            CoopNegReg({CI,LacI},{1,224,1,9,0.0005,0.0005},{bacterium}) from basicLibrary.plb
            UnReg({LacI},{0.5},{bacterium}) from basicLibrary.plb
            PostTransc({LacI},{0.00578,0.167,0.00116},{bacterium}) from basicLibrary.plb

            CoopNegReg({LacI,TetR},{1,224,1,9,0.0005,0.0005},{bacterium}) from basicLibrary.plb
            UnReg({TetR},{0.5},{bacterium}) from basicLibrary.plb
            PostTransc({TetR},{0.00578,0.167,0.00116},{bacterium}) from basicLibrary.plb

            CoopNegReg({TetR,CI},{1,224,1,9,0.0005,0.0005},{bacterium}) from basicLibrary.plb 
            UnReg({CI},{0.5},{bact}) from basicLibrary.plb
            PostTransc({CI},{0.00578,0.167,0.00116},{bacterium}) from basicLibrary.plb

        endRuleSet

    endRuleSets 

endSPsystem'''

Libraries of Modules in Systems Biology
---------------------------------------------------------------

In a **Systems biology scenario** modules can represent *basic regulatory mechanisms* or *regulatory motifs* in cellular systems that appear recurrently involving different  molecular species interacting according to characteristic rates in specific locations of the cells. For example, the following basic library defines modules representing *positve, negative and constitutive gene expression* as well as some basic transcriptional regulatory motifs in bacterial systems as *negative autoregulation (NAR)* and *incoherent feedforward loop (IFFL)*::

      libraryOfModules transcriptionalMotifs

         Const({X},{c_1},{l}) = 
         {
             r1: [ geneX ]_l -c_1-> [ geneX + rnaX ]_l 
         }

         PosReg({X,Y},{c_1,c_2,c_3},{l}) =
         {
             r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
             r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
             r3: [ proteinX_geneY ]_l -c_3-> [ proteinX_geneY + rnaY ]_l 
         }

         NegReg({X,Y},{c_1,c_2},{l}) =
         {
             r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
             r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
         }

         PostTransc({X},{c_1,c_2,c_3},{l}) =
         {
             r1: [ rnaX ]_l -c_1-> [ ]_l
             r2: [ rnaX ]_l -c_2-> [ rnaX + proteinX ]_l 
             r3: [ proteinX ]_l -c_3-> [ ]_l 
         }

         NAR({X},{c_1,c_2},{l}) =
         {
             NegReg({X,X},{c_1,c_2},{l}) from this
         }

         IFFL({X,Y,Z},{c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8},{l}) =
         {
             PosReg({X,Y},{c_1,c_2,c_3},{l}) from this
             PosReg({X,Z},{c_4,c_5,c_6},{l}) from this
             NegReg({Y,Z},{c_7,c_8},{l}) from this
          }

      endLibraryOfModules

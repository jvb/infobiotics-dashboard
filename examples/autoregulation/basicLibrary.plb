# Author: Francisco J. Romero-Campero #
# Date: May 2010 #
# Description: A library containing basic gene regulatory  mechanisms #

libraryOfModules basicLibrary

	# A module representing the unregulated expression of a gene X	#
	UnReg({X},{c_1 0:0.5:5 linear, c_2 0:0.01:0.1 linear, c_3 0:0.5:5 linear, c_4 0:0.01:0.1 linear},{l}) = 
		{
			rules:
                # Transcription of geneX #
				r1: [ geneX ]_l -c_1-> [ geneX + rnaX ]_l 
                # Degradation of the RNA #
                r2: [ rnaX ]_l -c_2-> [ ]_l
                # Translation of the RNA #
                r3: [ rnaX ]_l -c_3-> [ rnaX + proteinX ]_l
                # Degradation of the protein #
                r4: [ proteinX ]_l -c_4-> [ ]_l 
		}


	# A module representing the positive regulation of a protein X over a gene Y #
	PosReg({X,Y},{c_1 0:0.5:5 linear,c_2 0:0.5:5 linear,c_3 0:0.5:5 linear, c_4 0:0.01:0.1 linear, c_5 0:0.5:5 linear, c_6 0.05:0.01:1 linear},{l}) =
		{
			rules:
                # Binding and debinding of the transcription factor proteinX to geneY #
                r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
                r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
                # Transcription of geneY when proteinX is bound to its promoter # 
                r3: [ proteinX_geneY ]_l -c_3-> [ proteinX_geneY + rnaY ]_l
                # Degradation of the RNA #
                r4: [ rnaY ]_l -c_4-> [ ]_l
                # Translation of the RNA #
                r5: [ rnaY ]_l -c_5-> [ rnaY + proteinY ]_l
                # Degradation of the protein #    
                r6: [ proteinY ]_l -c_6-> [ ]_l 
		}


	# A module representing the negative regulation of a protein X over a gene Y #
	NegReg({X,Y},{c_1 0:0.5:5 linear, c_2 0:0.1:1 linear},{l}) =
		{
			rules:
                # Binding and debinding of the transcription factor proteinX to gene Y #
                r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
                r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
		}

endLibraryOfModules

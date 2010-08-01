# Author: Francisco J. Romero-Campero #
# Date: 14 May 2010 #
# Description: A library containing basic gene regulatory mechanisms # 

libraryOfModules basicLibrary

	# A module representing the unregulated expression of a gene X	#
	UnReg({X},{c_1 0:0.5:5 linear, c_2 0:0.01:0.1 linear, c_3 0:0.5:5 linear, c_4 0:0.01:0.1 linear},{l}) = 
		{
		rules:
		r1: [ geneX ]_l -c_1-> [ geneX + rnaX ]_l 
	      	r2: [ rnaX ]_l -c_2-> [ ]_l
   	   	r3: [ rnaX ]_l -c_3-> [ rnaX + proteinX ]_l 
   	   	r4: [ proteinX ]_l -c_4-> [ ]_l 
		}


	# A module representing the positive regulation of a protein X #
	# over a gene Y #
	PosReg({X,Y},{c_1 0:0.5:5 linear,c_2 0:0.5:5 linear,c_3 0:0.5:5 linear, c_4 0:0.01:0.1 linear, c_5 0:0.5:5 linear, c_6 0.05:0.01:1 linear},{l}) =
		{
		rules:
      		r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
     		r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
      		r3: [ proteinX_geneY ]_l -c_3-> [ proteinX_geneY + rnaY ]_l 
	      	r4: [ rnaX ]_l -c_4-> [ ]_l
   	   	r5: [ rnaX ]_l -c_5-> [ rnaX + proteinX ]_l 
   	   	r6: [ proteinX ]_l -c_6-> [ ]_l 
		}


	# A module representing the negative regulation of a protein X	#
	# over a gene Y	#
	NegReg({X,Y},{c_1 0:0.5:5 linear, c_2 0:0.1:1 linear},{l}) =
		{
		rules:
	      	r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
   	   	r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
		}

endLibraryOfModules

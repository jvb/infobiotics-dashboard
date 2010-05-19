# Author: Francisco J. Romero-Campero 										#
# Date: 14 May 2010						  										#
# Description: A library containing basic gene regulatory   		#
#					mechanisms 														#

libraryOfModules basicLibrary

	# A module representing the unregulated expression of a gene X	#
	UnReg({X},{c_1},{l}) = 
		{
			rules:
				r1: [ geneX ]_l -c_1-> [ geneX + rnaX ]_l 
		}


	# A module representing the positive regulation of a protein X #
	# over a gene Y																#
	PosReg({X,Y},{c_1,c_2,c_3},{l}) =
		{
			rules:
      		r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
     			r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
      		r3: [ proteinX_geneY ]_l -c_3-> [ proteinX_geneY + rnaY ]_l 
		}


	# A module representing the negative regulation of a protein X	#
	# over a gene Y																#
	NegReg({X,Y},{c_1,c_2},{l}) =
		{
			rules:
	      	r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
   	   	r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
		}

	# A module representing the cooperative regulation of a protein#
	# X over a gene Y 															#
	CoopNegReg({X,Y},{c_1,c_2,c_3,c_4,c_5,c_6},{l}) =
		{
			rules:
	      	r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
	      	r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
	      	r3: [ proteinX + proteinX_geneY ]_l -c_3-> [ proteinX2_geneY ]_l 
	      	r4: [ proteinX2_geneY ]_l -c_4-> [ proteinX + proteinX_geneY ]_l 
	      	r5: [ proteinX_geneY ]_l -c_5-> [ proteinX_geneY + rnaY ]_l 
	      	r6: [ proteinX2_geneY ]_l -c_6-> [ proteinX2_geneY + rnaY ]_l 
		}

	# A module representing some post transcriptional processes 	#
	#such as rna degradation, translation and protein degradation  #
	PostTransc({X},{c_1,c_2,c_3},{l}) = 
		{
			rules:
	      	r1: [ rnaX ]_l -c_1-> [ ]_l
   	   	r2: [ rnaX ]_l -c_2-> [ rnaX + proteinX ]_l 
   	   	r3: [ proteinX ]_l -c_3-> [ ]_l 
		}

endLibraryOfModules

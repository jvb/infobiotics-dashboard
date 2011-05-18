libraryOfModules basicLibrary

	UnReg({X},{c_1},{l}) = 
		{
			rules:
				r1: [ geneX ]_l -c_1-> [ geneX + rnaX ]_l 
		}

	PosReg({X,Y},{c_1,c_2,c_3},{l}) =
		{
			rules:
		      	r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
	     		r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
	    	  	r3: [ proteinX_geneY ]_l -c_3-> [ proteinX_geneY + rnaY ]_l 
		}

	NegReg({X,Y},{c_1,c_2},{l}) =
		{
			rules:
		      	r1: [ proteinX + geneY ]_l -c_1-> [ proteinX_geneY ]_l 
		      	r2: [ proteinX_geneY ]_l -c_2-> [ proteinX + geneY ]_l 
		}

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

	PostTransc({X},{c_1,c_2,c_3},{l}) = 
		{
			rules:
		      	r1: [ rnaX ]_l -c_1-> [ ]_l
		      	r2: [ rnaX ]_l -c_2-> [ rnaX + proteinX ]_l 
		      	r3: [ proteinX ]_l -c_3-> [ ]_l 
		}

endLibraryOfModules

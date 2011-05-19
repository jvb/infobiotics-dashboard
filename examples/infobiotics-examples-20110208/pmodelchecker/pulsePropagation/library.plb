libraryOfModules promoterLibrary

	Pconst({X},{c_1},{l}) = 
		{
			rules:
				r1: [ Pconst_geneX ]_l -c1-> [ Pconst_geneX + rnaX_RNAP ]_l		c1 = 2
		}      

	Plux({X},{c_1, c_2, c_3},{l}) =
		{
			rules:
      	r1: [ LuxR2 + Plux_geneX ]_l -c_1-> [ Plux_LuxR2_geneX ]_l
      	r2: [ Plux_LuxR2_geneX ]_l -c_2-> [ LuxR2 + Plux_geneX ]_l 
      	r3: [ Plux_LuxR2_geneX ]_l -c_3-> [ Plux_LuxR2_geneX + rnaX_RNAP ]_l 
		}

	Pluxleaky({X},{c_1,c_2,c_3,c_4},{l}) =
		{
			rules:
			r1: [ LuxR2 + Plux_geneX ]_l -c_1-> [ Plux_LuxR2_geneX ]_l 
      	r2: [ Plux_LuxR2_geneX ]_l -c_2-> [ LuxR2 + Plux_geneX ]_l
      	r3: [ Plux_LuxR2_geneX ]_l -c_3-> [ Plux_LuxR2_geneX + rnaX_RNAP ]_l
			r4: [ Plux_geneX ]_l -c_4-> [ Plux_geneX + rnaX_RNAP ]_l 
		}

	PluxPR({X},{c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9},{l}) =
		{
			rules:
			r1: [ LuxR2 + PluxPR_geneX ]_l -c_1-> [ PluxPR_LuxR2_geneX ]_l 
      	r2: [ PluxPR_LuxR2_geneX ]_l -c_2-> [ LuxR2 + PluxPR_geneX ]_l 
			r3: [ LuxR2 + PluxPR_CI2_geneX ]_l -c_3-> [ PluxPR_LuxR2_CI2_geneX ]_l
			r4: [ PluxPR_LuxR2_CI2_geneX ]_l -c_4-> [ LuxR2 + PluxPR_CI2_geneX ]_l
			r5: [ CI2 + PluxPR_geneX ]_l -c_5-> [ PluxPR_CI2_geneX ]_l
			r6: [ PluxPR_CI2_geneX ]_l -c_6-> [ CI2 + PluxPR_geneX ]_l
			r7: [ CI2 + PluxPR_LuxR2_geneX ]_l -c_7-> [ PluxPR_LuxR2_CI2_geneX ]_l 
      	r8: [ PluxPR_LuxR2_CI2_geneX ]_l -c_8-> [ CI2 + PluxPR_LuxR2_geneX ]_l 
			r9: [ PluxPR_LuxR2_geneX ]_l -c_9-> [ PluxPR_LuxR2_geneX + rnaX_RNAP ]_l
		}

	Plac({X},{c_1,c_2,c_3},{l}) =
		{
			rules:
			r1: [ Plac_geneX ]_l -c_1-> [ Plac_geneX + rnaX_RNAP ]_l
			r2: [ proteinLacI + Plac_geneX ]_l -c_2-> [ Plac_LacI_geneX ]_l
			r3: [ Plac_LacI_geneX ]_l -c_3-> [ proteinLacI + Plac_geneX ]_l
      	r4: [ proteinUnLacI + Plac_geneX ]_l -c_2-> [ Plac_UnLacI_geneX ]_l 
			r5: [ Plac_UnLacI_geneX ]_l -c_3-> [ proteinUnLacI + Plac_geneX ]_l
		}

	PluxPtetR({X},{c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9,c_10,c_11,c_12,c_13,c_14,c_15},{l}) =
		{
			rules:
      	r1:  [ LuxR2 + PluxPtetR_geneX ]_l -c_1-> [ PluxPtetR_LuxR2_geneX ]_l
      	r2:  [ PluxPtetR_LuxR2_geneX ]_l -c_2-> [ LuxR2 + PluxPtetR_geneX ]_l
      	r3:  [ LuxR2 + PluxPtetR_TetR_geneX ]_l -c_3-> [ PluxPtetR_LuxR2_TetR_geneX ]_l
      	r4:  [ PluxPtetR_LuxR2_TetR_geneX ]_l -c_4-> [ LuxR2 + PluxPtetR_TetR_geneX ]_l
      	r5:  [ LuxR2 + PluxPtetR_TetR2_geneX ]_l -c_5-> [ PluxPtetR_LuxR2_TetR2_geneX ]_l
      	r6:  [ PluxPtetR_LuxR2_TetR2_geneX ]_l -c_6-> [ LuxR2 + PluxPtetR_TetR2_geneX ]_l
      	r7:  [ TetR + PluxPtetR_geneX ]_l -c_7-> [ PluxPtetR_TetR_geneX ]_l
      	r8:  [ PluxPtetR_TetR_geneX ]_l -c_8-> [ TetR + PluxPtetR_geneX ]_l
      	r9:  [ TetR + PluxPtetR_LuxR2_geneX ]_l -c_9-> [ PluxPtetR_LuxR2_TetR_geneX ]_l
      	r10: [ PluxPtetR_LuxR2_TetR_geneX ]_l -c_10-> [ TetR + PluxPtetR_LuxR2_geneX ]_l
      	r11: [ TetR + PluxPtetR_TetR_geneX ]_l -c_11-> [ PluxPtetR_TetR2_geneX ]_l
      	r12: [ PluxPtetR_TetR2_geneX ]_l -c_12-> [ TetR + PluxPtetR_TetR_geneX ]_l
      	r13: [ TetR + PluxPtetR_LuxR2_TetR_geneX ]_l -c_13-> [ PluxPtetR_LuxR2_TetR2_geneX ]_l
      	r14: [ PluxPtetR_LuxR2_TetR2_geneX ]_l -c_14-> [ TetR + PluxPtetR_LuxR2_TetR_geneX ]_l
      	r15: [ PluxPtetR_LuxR2_geneX ]_l -c_15-> [ PluxPtetR_LuxR2_geneX + rnaX_RNAP ]_l
		}

	PR({X},{c_1,c_2,c_3},{l}) =
		{
			rules:
				r1: [ PR_geneX ]_l -c_1-> [ PR_geneX + rnaX_RNAP ]_l
				r2: [ CI2 + PR_geneX ]_l -c_2-> [ PR_CI2_geneX ]_l
				r3: [ PR_CI2_geneX ]_l -c_3-> [ CI2 + PR_geneX ]_l
		}

	PostTransc({X},{c_1,c_2,c_3,c_4,c_5},{l}) =
		{
			rules:
				r1: [ rnaX_RNAP ]_l -c_1-> [ rnaX ]_l
				r2: [ rnaX ]_l -c_2-> [ rnaX + proteinX_Rib ]_l
				r3: [ rnaX ]_l -c_3-> [ ]_l
				r4: [ proteinX_Rib ]_l -c_4-> [ proteinX ]_l
				r5: [ proteinX ]_l -c_5-> [ ]_l
		}

	Dim({X,Y},{c_1,c_2},{l}) =
		{
			rules:
				r1: [ proteinX + proteinX ]_l -c_1-> [ Y ]_l
	      		r2: [ Y ]_l -c_2-> [ ]_l
		}

	DimSig({X,S,Y},{c_1,c_2,c_3,c_4},{l}) =
		{
			rules:
		      	r1: [ proteinX + signalS ]_l -c_1-> [ proteinX_S ]_l
		      	r2: [ proteinX_S ]_l -c_2-> [ ]_l
		      	r3: [ proteinX_S + proteinX_S ]_l -c_3-> [ Y ]_l
		      	r4: [ Y ]_l -c_4-> [ ]_l
		}

	Diffusion({X},{c_1},{l}) = 
		{
			rules:
		      	r1: [ signalX ]_l =(1,0)=[ ] -c_1-> [ ]_l =(1,0)=[ signalX ]
		      	r2: [ signalX ]_l =(-1,0)=[ ] -c_1-> [ ]_l =(-1,0)=[ signalX ]
		      	r3: [ signalX ]_l =(0,1)=[ ] -c_1-> [ ]_l =(0,1)=[ signalX ]
		      	r4: [ signalX ]_l =(0,-1)=[ ] -c_1-> [ ]_l =(0,-1)=[ signalX ]
		}

	Deg({X},{c_1},{l}) =
		{
			rules:
      			r1: [ X ]_l -c_1-> [ ]_l
		}

	pulseGenerator({X},{c_1,c_2,c_3,c_4,c_5},{l}) =
		{
				Pconst({LuxR},{0.1},{l}) from this 
				PostTransc({LuxR},{3.2,0.3,0.04,3.6,0.075},{l}) from this
				DimSig({LuxR,3OC12,LuxR2},{1,0.0154,1,0.0154},{l}) from this
	
				Plux({CI},{1,1,4},{l}) from this
				PostTransc({CI},{3.2,0.02,0.04,3.6,0.1},{l}) from this
				Dim({CI,CI2},{1,0.00554},{l}) from this
	
				PluxPR({X},{1,1,1,1,5,0.0000001,5,0.0000001,4},{l}) from this
				PostTransc({X},{c_1,c_2,c_3,c_4,c_5},{l}) from this
	
	        	Diffusion({3OC12},{0.1},{l}) from this
		}

endLibraryOfModules

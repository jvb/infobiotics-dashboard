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

         Diffusion({3OC12},{0.5},{bacterium}) from library.plb

      endRuleSet

   endRuleSets

endSPsystem

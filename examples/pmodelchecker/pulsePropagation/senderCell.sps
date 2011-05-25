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

			r1: [ proteinLuxI ]_cell -c1-> [ proteinLuxI + signal3OC12 ]_cell						c1 = 1

      	r2: [ signal3OC12 ]_cell =(1,0)=[ ] -c2-> [ ]_cell =(1,0)=[ signal3OC12 ]			c2 = 2
      	r3: [ signal3OC12 ]_cell =(-1,0)=[ ] -c3-> [ ]_cell =(-1,0)=[ signal3OC12 ]		c3 = 2
      	r4: [ signal3OC12 ]_cell =(0,1)=[ ] -c2-> [ ]_cell =(0,1)=[ signal3OC12 ]			c4 = 2
      	r5: [ signal3OC12 ]_cell =(0,-1)=[ ] -c2-> [ ]_cell =(0,-1)=[ signal3OC12 ]		c5 = 2



		endRuleSet

	endRuleSets

endSPsystem

SPsystem positiveAutoregulation
 
	alphabet
		gene1
		protein1
		protein1_gene1
		rna1
	endAlphabet

   compartments
		bacterium
   endCompartments
      
   initialMultisets
     initialMultiset bacterium
       gene1 1
     endInitialMultiset
   endInitialMultisets

  	ruleSets
		
		ruleSet bacterium	
			UnReg({1},{0.0025},{bacterium}) from basicLibrary.plb
			PosReg({1,1},{1,0.6022,0.025},{bacterium}) from basicLibrary.plb
			PostTransc({1},{0.07,3,0.01},{bacterium}) from basicLibrary.plb
		endRuleSet

	endRuleSets 

endSPsystem

SPsystem negativeAutoregulation
 
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
			NAR({1},{3,1,0.8},{bacterium}) from motifLibrary.plb
			PostTransc({1},{0.07,3,0.01},{bacterium}) from basicLibrary.plb
		endRuleSet

	endRuleSets 

endSPsystem

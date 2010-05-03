SPsystem Boundary

	alphabet
		signal3OC12
   endAlphabet

   compartments
		cell
	endCompartments

   initialMultisets
		initialMultiset cell
		endInitialMultiset
   endInitialMultisets

   ruleSets
		ruleSet cell
         Deg({signal3OC12},{0.075},{cell}) from library.plb
		endRuleSet
   endRuleSets      

endSPsystem


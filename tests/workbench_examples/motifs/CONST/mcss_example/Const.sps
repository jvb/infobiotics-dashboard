# Author: Francisco J. Romero-Campero 								#
# Date: 14 May 2010						  								#
# Description: A model of a gene constitutively expressed   #

SPsystem constitutiveExpression
 
	# Molecular species in the system #
	alphabet
		gene1
		protein1
		rna1
	endAlphabet

	# The system consists of a single compartment #
   compartments
		bacterium
   endCompartments
      
	# The initial number of molecules present in the system #
   initialMultisets
     initialMultiset bacterium
       gene1 1
     endInitialMultiset
   endInitialMultisets

	# The rules representing the molecular interactions #
  	ruleSets
		
		ruleSet bacterium	

			# Constitutive expression of gene1 #
			UnReg({1},{0.025},{bacterium}) from basicLibrary.plb

			# Post trasncriptional processes associated to gene1 #
			PostTransc({1},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

		endRuleSet

	endRuleSets 

endSPsystem

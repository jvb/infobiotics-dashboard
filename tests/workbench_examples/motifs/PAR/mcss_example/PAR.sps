# Author: Francisco J. Romero-Campero 										#
# Date: 14 May 2010						  										#
# Description: A model of a gene that regulates itself positively #

SPsystem negativeAutoregulation

	# Molecular species in the system # 
	alphabet
		gene1
		protein1
		protein1_gene1
		rna1
	endAlphabet

	# The system consists of a single compartment #
   compartments
		bacterium
   endCompartments
      
	# Initial number of molecules present in the system #
   initialMultisets
     initialMultiset bacterium
       gene1 1
     endInitialMultiset
   endInitialMultisets

	# Rules describing the molecular interactions in the system #
  	ruleSets
		
		ruleSet bacterium	

			# Baseline production of gene 1 #
			UnReg({1},{0.0025},{bacterium}) from basicLibrary.plb

			# Positive autoregulation #
			PosReg({1,1},{1,0.6022,0.025},{bacterium}) from basicLibrary.plb

			# Post trasncriptional regulation #
			PostTransc({1},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

		endRuleSet

	endRuleSets 

endSPsystem

# Author: Francisco J. Romero-Campero 							  #
# Date: 14 May 2010						  						  #
# Description: A model of a gene that regulates itself negatively #

SPsystem negativeAutoregulation
 
	# Molecular species in the system #
	alphabet
		gene1
		protein1
		protein1_gene1
		rna1
	endAlphabet

	# The system consists of a single compartment called bacterium #
   compartments
		bacterium
   endCompartments
      
	# The initial number of molecules present in the system #
   initialMultisets
     initialMultiset bacterium
       gene1 1
     endInitialMultiset
   endInitialMultisets

	# The rules describing the molecular interactions in the different compartmenst of the system #
  	ruleSets
		
		ruleSet bacterium	

			# Unregulated expression of gene 1 #
			UnReg({1},{0.13,0.002,0.04,0.000578},{bacterium}) from basicLibrary.plb

			# Negative regulation of gene 1 by the protein product of gene 1 #
			NegReg({1,1},{0.056,0.147},{bacterium}) from basicLibrary.plb

		endRuleSet

	endRuleSets 

endSPsystem

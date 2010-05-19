# Author: Francisco J. Romero-Campero 										#
# Date: 14 May 2010						  										#
# Description: A model of a gene that regulates itself negatively #

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
      
	# The initial number of molecules present in the system #
   initialMultisets
     initialMultiset bacterium
       gene1 1
     endInitialMultiset
   endInitialMultisets

	# The rules describing the molecular interactions in the system #
  	ruleSets
		
		ruleSet bacterium	

			# Negative autoregulation of gene 1 #
			NAR({1},{3,1,0.8},{bacterium}) from motifLibrary.plb

			# Processes for the post trasncriptional regulation of gene 1 #
			PostTransc({1},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

		endRuleSet

	endRuleSets 

endSPsystem

# Author: Francisco J. Romero-Campero 							  #
# Date: July 2010						  						  #
# Description: A model of a gene expressed constitutively #

SPsystem negativeAutoregulation
 
	# Molecular species in the system #
	alphabet
		gene1
		protein1
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

		# Molecular interactions involving the compartment bacterium #		
		ruleSet bacterium	

			# Unregulated expression of gene 1 #
			UnReg({1},{0.025,0.07,3,0.01},{bacterium}) from basicLibrary.plb

		endRuleSet

	endRuleSets 

endSPsystem

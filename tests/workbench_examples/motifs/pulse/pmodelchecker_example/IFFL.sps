# Author: Francisco J. Romero-Campero 										#
# Date: 14 May 2010						  										#
# Description: A model of three genes forming an incoherent feed	#
#					forward loop													#

SPsystem IFFL

	# Molecular species in the system # 
	alphabet
		gene1
		gene2
		gene3
		protein1
		protein1_gene2
		protein1_gene3
		protein2
		protein2_gene3
		protein3
		rna1
		rna2
		rna3
	endAlphabet

	# The system consists of a single compartment #
   compartments
		bacterium
   endCompartments
      
	# Initial number of molecules present in the system #
   initialMultisets
     initialMultiset bacterium
       gene1 	1
		 gene2	1
		 gene3	1
     endInitialMultiset
   endInitialMultisets

	# Rules describing the molecular interactions in the system #	
  	ruleSets
		
		ruleSet bacterium	

			# Constitutive expression of gene 1 #
			UnReg({1},{0.025},{bacterium}) from basicLibrary.plb
			PostTransc({1},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

			# Positive regulation of gene 1 over gene 2 #
			PosReg({1,2},{0.1,0.1,0.025},{l}) from basicLibrary.plb
			PostTransc({2},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

			# Positive regulation of gene 1 over gene 3 #
			PosReg({1,3},{1,1,0.25},{l}) from basicLibrary.plb
			PostTransc({3},{0.07,3,0.01},{bacterium}) from basicLibrary.plb

			# Negative regulation of gene 2 over gene 3 #
			NegReg({2,3},{1,0.001},{bacterium}) from basicLibrary.plb

		endRuleSet

	endRuleSets 

endSPsystem

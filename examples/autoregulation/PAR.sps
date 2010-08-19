# Author: Francisco J. Romero-Campero 							  #
# Date: July 2010						  						  #
# Description: A model of a gene that regulates itself positively #

SPsystem negativeAutoregulation
 
	# Molecular species in the system #
	alphabet
		gene1
		protein1
		protein1_gene1
		rna1
		signal1
	endAlphabet

	# The system consists of a single compartment called bacterium #
   compartments
		media
		bacterium inside media
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
			UnReg({1},{0.0025,0.07,3,0.01},{bacterium}) from basicLibrary.plb

			# Positive regulation of gene 1 by the protein product of gene 1 #
			PosReg({1,1},{1,0.6022,0.025,0.07,3,0.01},{bacterium}) from basicLibrary.plb

			# Protein1 is an enzyme that synthesizes signal 1 #
			r1: [ protein1 ]_bacterium -c1-> [ protein1 + signal1 ]_bacterium 					c1 = 0.001

			# Signal1 diffuses freely outside bacteria #		
			r2: [ signal1 ]_bacterium -c2-> signal1 [ ]_bacterium										c2 = 0.001

			# Singal1 can be degraded inside bacteria #
			r3: [ signal1 ]_bacterium -c3-> [ ]_bacterium												c3 = 0.0001

		endRuleSet

		# Molecular interactions involving the compartment media #
		ruleSet media

			# Signal1 diffuses freely inside bacteria #
			r1: signal1 [ ]_bacterium -c1-> [ signal1 ]_bacterium										c1 = 0.001

			# Signal1 can be degraded in the media #
			r2: [ signal1 ]_bacterium -c2-> [ ]_bacterium												c2 = 0.0001

			# Signal1 diffuses freely to neighboruing media #
     		r3: [ signal1 ]_l =(1,0)=[ ] -c3-> [ ]_l =(1,0)=[ signal1 ]								c3 = 0.00025
     		r4: [ signal1 ]_l =(-1,0)=[ ] -c3-> [ ]_l =(-1,0)=[ signal1 ]							c3 = 0.00025
     		r5: [ signal1 ]_l =(0,1)=[ ] -c3-> [ ]_l =(0,1)=[ signal1 ]								c3 = 0.00025
     		r6: [ signal1 ]_l =(0,-1)=[ ] -c3-> [ ]_l =(0,-1)=[ signal1 ]							c3 = 0.00025
		
		endRuleSet

	endRuleSets 

endSPsystem

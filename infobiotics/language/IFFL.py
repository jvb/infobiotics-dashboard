# Jonathan Blakes
# 15th June 2010

from sps import SPsystem, Compartment
from plb import * 

label = 'bacterium'

class IFFL(SPsystem):
    ''' A model of three genes forming an incoherent feed forward loop. '''
    
    name = 'negativeAutoregulation'
    
    compartments = [
        Compartment(label=label),
    ]
    
    initialMultisets = dict(
        bacterium=dict(
            gene1=1,
            gene2=2,
            gene3=3,
        ),
    )
    
    ruleSets = {
        label:[
            
            # Constitutive expression of gene 1
            UnReg('gene1', 'rna1', 0.025, label),
            PostTransc('gene1', 'protein1', 0.07, 3, 0.01, label),
            
            # Positive regulation of gene 1 over gene 2
            PosReg('protein1', 'gene2', 'rna2', 0.1, 0.1, 0.025, label),
            PostTransc('rna2', 'protein2', 0.07, 3, 0.01, label),
            
            # Positive regulation of gene 1 over gene 3 #
#            PosReg({1,3},{1,1,0.25},{bacterium}) from basicLibrary.plb
#            PostTransc({3},{0.07,3,0.01},{bacterium}) from basicLibrary.plb
            PosReg('protein1', 'gene3', 'rna3', 1, 1, 0.25, label),
            PostTransc('rna3', 'protein3', 0.07, 3, 0.01, label),

            # Negative regulation of gene 2 over gene 3 #
            NegReg('protein2', 'gene3', 1, 0.001, label),
        ],
    }
    
print IFFL().alphabet    